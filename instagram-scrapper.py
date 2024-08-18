from selenium import webdriver
import time
import sys
from selenium.webdriver.common.by import By
import pandas as pd
import os

def convertAndSave(batch, usernames, comments, i):
    print(f"SAVING current batch : {batch}")
    try:
        df = pd.DataFrame({
            "username": usernames,
            "comment": comments
        })
    except:
        min_length = min(len(usernames), len(comments))
        usernames = usernames[:min_length]
        comments = comments[:min_length]

        df = pd.DataFrame({
            "username": usernames,
            "comment": comments
        })
    csv_path = os.path.join('./', f'postFolkative{i}-batch_{batch}.csv')
    df.to_csv(csv_path, index=True, encoding='utf-8')
    print(df.head(100))

def scrapeall(starting_url, comments_limit):
    path = r"C:\Code Installer\msedgedriver.exe"
    service = webdriver.EdgeService(executable_path = path)
    driver = webdriver.Edge(service= service)

    url="https://www.instagram.com/"
    driver.get(url) 
    time.sleep(2)

    username=driver.find_element(By.NAME,"username")
    username.send_keys ('wingunstore')

    password =driver.find_element (By.NAME,"password")
    password.send_keys('wingun003')
    password.submit()
    time.sleep(5)

    for i in range(len(starting_url)):
        driver.get(starting_url[i])
        driver.set_script_timeout(24 * 60 * 60)  # Timeout in seconds (1 days)
        time.sleep(5)
        try:
            print("init all params")
            scrollable_element = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[2]')
            last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
            
            df = pd.DataFrame(columns=["username", "comment"])
            usernames = []
            comments = []
            retry_counter = 0
            retry_locater = 0 
            batch = 0
            
            checkpoints = 0
            increase_checkpoints = 0

            while True:
                comment_block = driver.find_elements(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div')
                print(f"current observable : {len(comment_block)}")

                if len(usernames) >= (2000*(batch+1)) or len(comment_block) >= (2020*(batch+1)):
                    batch += 1
                    convertAndSave(batch, usernames, comments, i)

                if len(comment_block) > increase_checkpoints:
                    batch_limit = len(comment_block)-checkpoints
                    print(f"{len(comment_block)} observable comments")
                    print(f"{batch_limit} query to add")
                    for j in range(batch_limit): # COBA INI BANG
                        if increase_checkpoints >= comments_limit[i] or (j >= batch_limit-1):
                            break
                        
                        try:
                            usernames.append(driver.find_element(By.XPATH,f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div[{checkpoints+1}]/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/span[1]/span/div/a/div/div/span').text) 
                            comments.append(driver.find_element(By.XPATH,f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div[{checkpoints+1}]/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/span').text)
                            checkpoints += 1
                        except Exception as e:
                            print(f"checkpoints >> {checkpoints+1}")
                            if retry_locater > 1:
                                print("try to look up --------------------")
                                try: # try to access forward div
                                    lookup = driver.find_element(By.XPATH,f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div[{checkpoints+2}]/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/span[1]/span/div/a/div/div/span').text
                                    checkpoints += 1

                                    usernames.append(lookup)
                                    comments.append(driver.find_element(By.XPATH,f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div[{checkpoints+1}]/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/span').text)
                                    retry_locater = 0
                                    continue
                                except:
                                    print("skipping --------------------")
                                    checkpoints += 2
                                    retry_locater = 0
                                    continue
                            retry_locater += 1
                            time.sleep(0.5)
                            continue
                    print(f" username collected >> {len(usernames)} | checkpoints >> {checkpoints}")
                    increase_checkpoints = increase_checkpoints + 500
                    print(f" next limit >> {increase_checkpoints}")

                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 2000;", scrollable_element)
                time.sleep(1)
                                
                new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
                scroll_top = driver.execute_script("return arguments[0].scrollTop", scrollable_element)
                
                if new_height == last_height and scroll_top + scrollable_element.size['height'] >= new_height:
                    if retry_counter == 3:
                        print("end of scrollable_element")
                        convertAndSave(batch, usernames, comments, i)
                        break
                    time.sleep(3)
                    retry_counter += 1
                    continue
                else:
                    retry_counter = 0
                last_height = new_height
        except Exception as e:
            print(e)
            pass
    driver.close()

POST_SOURCE_URL = ["https://www.instagram.com/p/C9BwqoKv2Om/?igsh=cHNmNTJmdHhyZ3Bn","https://www.instagram.com/p/C8_F3_UPjqF/?igsh=MWplZWVxNTh3ZHQ2bA%3D%3D","https://www.instagram.com/p/C9PbJnAPSz4/?igsh=dmt5Yzd4c2gwdWY%3D","https://www.instagram.com/p/C8ePvHOPLMM/?igsh=N2tjZmQ5dXl4eGJy","https://www.instagram.com/p/C8b25jaPTU8/?igsh=MWFlMjU4bXkxeXdpdA%3D%3D"]
POST_COMMENTS_LIMIT = [5000, 5000, 5000, 5000, 5000] 
scrapeall(POST_SOURCE_URL, POST_COMMENTS_LIMIT)