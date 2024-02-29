import os
import subprocess
from time import sleep

import selenium.webdriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

num_input_path = "#app > div > div > div._2QgSC > div._2Ts6i._3RGKj._318SY > span > div > span > div > " \
                 "div._1tRmd._3wQ5i.o7fBL > div._1EUay > div._2vDPL > div > div > p"

resulting_path = "#app > div > div > div._2QgSC > div._2Ts6i._3RGKj._318SY > span > div > span > div > " \
                 "div.g0rxnol2.g0rxnol2.thghmljt.p357zi0d"

result_num_path = "#app > div > div > div._2QgSC > div._2Ts6i._3RGKj._318SY > span > div > span > div > " \
                  "div.g0rxnol2.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.ag5g9lrv.bs7a17vp" \
                  ".ov67bkzj > div._199zF._3j691"

loading = "#app > div > div > div._2QgSC > div._2Ts6i._3RGKj._318SY > span > div > span > div > " \
          "div._1tRmd._3wQ5i.o7fBL > div._1EUay > span > div"

# some variables :) :) :)
num_input = None

output_template_1 = """
Number: [number]/[total]    |    Status: [phone_num]=>[status]
Existing: [existing]    |    Non-existing: [non-existing]
"""

output_template_2 = """
Number: [number]/[total]    |    Status: [phone_num]=>[status]
Existing: [existing]    |    Non-existing: [non-existing]
"""


class WhatsAppBot:
    def __init__(self):
        self.verification_mode = 1
        self.program = None
        self.driver = None
        self.total_numbers = 0
        self.existing_numbers = 0
        self.non_existing_numbers = 0
        self.number_list_to_verify = []

    def start(self):
        self.program = subprocess.Popen(
            '"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 '
            '--user-data-dir=C:\Development\localhost'
        )
        options = uc.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = uc.Chrome(options=options)

    def goto_whatsapp(self):
        self.driver.get("https://web.whatsapp.com/")

    def goto_new_chat(self):
        while True:
            try:
                new_chat_button = self.driver.find_element(By.XPATH,
                                                           '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div')
                new_chat_button.click()
                break
            except:
                pass

    def input_number(self, number):
        global num_input
        if not num_input:
            num_input = self.driver.find_element(By.CSS_SELECTOR, num_input_path)
        num_input.send_keys(Keys.CONTROL + "a" + Keys.DELETE)
        num_input.send_keys(str(number) if type(number) == int else number)

    def check_loader(self):
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, "_38r4-")
            except:
                break

    def number_exists(self, num_index):
        result_no = self.driver.find_element(By.CSS_SELECTOR, resulting_path)
        if "no results" in result_no.text.lower():
            self.non_existing_numbers += 1
            return False
        else:
            self.existing_numbers += 1
            return True

    def start_getting_numbers(self, excel_bot):
        for i, num in enumerate(self.number_list_to_verify):
            self.input_number(num)
            sleep(1)
            self.check_loader()
            if self.number_exists(num):
                excel_bot.write_to_workbook(num, "existing")
                status = "existing"
            else:
                status = "non-existing"
            os.system("cls" if os.name == "nt" else "clear")
            print(
                output_template_2.replace("[number]", str(i + 1)).replace(
                    "[total]",
                    str(len(self.number_list_to_verify))
                ).replace("[existing]", str(self.existing_numbers)).replace(
                    "[non-existing]", str(self.non_existing_numbers)
                ).replace(
                    "[phone_num]",
                    str(num)
                ).replace("[status]", status)
            )
            with open("numbers.txt", "r+") as f:
                lines = f.readlines()
                f.seek(0)
                f.truncate()
                f.writelines(lines[1:])

        print(f"Total numbers found: {self.existing_numbers}")

    def quit(self):
        # delete excel_file_path.txt and numbers.txt
        os.remove("numbers.txt")
        os.remove("excel_file_path.txt")
        self.program.kill()
        self.driver.quit()
