import subprocess
from time import sleep

import selenium.webdriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

program = subprocess.Popen(
    '"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 '
    '--user-data-dir=C:\Development\localhost'
)



num_input_path = "#app > div > div > div._2QgSC > div._2Ts6i._3RGKj._318SY > span > div > span > div > " \
                 "div._1tRmd._3wQ5i.o7fBL > div._1EUay > div._2vDPL > div > div > p"

resulting_path = "#app > div > div > div._2QgSC > div._2Ts6i._3RGKj._318SY > span > div > span > div > " \
                 "div.g0rxnol2.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.ag5g9lrv.bs7a17vp" \
                 ".ov67bkzj > div > div > span"

result_num_path = "#app > div > div > div._2QgSC > div._2Ts6i._3RGKj._318SY > span > div > span > div > " \
                  "div.g0rxnol2.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.ag5g9lrv.bs7a17vp" \
                  ".ov67bkzj > div._199zF._3j691"

loading = "#app > div > div > div._2QgSC > div._2Ts6i._3RGKj._318SY > span > div > span > div > div._1tRmd._3wQ5i.o7fBL > div._1EUay > span > div"

try:
    with open("currentnumber.txt", "r") as file:
        start_num = int(file.read())
except FileNotFoundError:
    start_num = int(input("Enter the starting number: "))  # 447947030019
total_num = int(input("Enter the total number to check (or leave blank for 10000): "))  # 50

if not total_num:
    total_num = 10000

options = uc.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = uc.Chrome(options=options)
driver.get("https://web.whatsapp.com/")
while True:
    try:
        new_chat_button = driver.find_element(By.XPATH, '//*[@data-icon="new-chat"]')
        new_chat_button.click()
        break
    except:
        pass
while True:
    try:
        num_input = driver.find_element(By.CSS_SELECTOR, num_input_path)
        break
    except:
        pass

for i in range(total_num):
    num_input.send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    num_input.send_keys(start_num)
    sleep(0.1)
    while True:
        try:
            driver.find_element(By.CLASS_NAME, "_38r4-")
        except:
            break
    try:
        result_no = driver.find_element(By.CSS_SELECTOR, resulting_path)
        if "no results" in result_no.text.lower():
            print(f"{start_num} does not exists")
        # print(f"{start_num} does not exists")
    except:
        print(f"{start_num} exists")
    start_num += 1
input("Enter to exit")
program.kill()
