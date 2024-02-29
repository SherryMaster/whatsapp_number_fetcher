import random
from time import sleep
from bot import WhatsAppBot
from excel import ExcelBot
from tkinter import filedialog, messagebox
import os
import winsound

excel = ExcelBot()
verify_mode = 1

continue_from_last = False

if os.path.isfile("numbers.txt"):
    with open("numbers.txt", "r") as f:
        total_numbers = len(f.read().split("\n"))
    continue_from_last = messagebox.askyesno(title="Continue from last", message=f"Last unfinished process found. Start from there?\n"
                                                                                 f"Total numbers remaining: {total_numbers}")

if continue_from_last:
    with open("numbers.txt", "r") as f:
        content = f.read().split("\n")
        number_list_to_verify = content
        print("Numbers: " + str(number_list_to_verify))
        total_numbers = len(number_list_to_verify)
        print("\n\n\nTotal numbers remaining: " + str(total_numbers))
    with open("excel_file_path.txt", "r") as f:
        excel.excel_file_path = f.read()
    excel.load_a_workbook(excel.excel_file_path)
    verify_mode = 3
else:
    create_sheet = input("Type 'y' to create a new sheet or any other key to select an existing one: ")
    if create_sheet == "y":
        folder = filedialog.askdirectory(title="Select folder to save file")
        file_name = input("Enter file name: ")
        excel.create_workbook(folder, file_name)
        with open("excel_file_path.txt", "w") as f:
            f.write(excel.excel_file_path)
    else:
        excel_file_path = filedialog.askopenfilename(title="Select Excel file", filetypes=(("Excel files", "*.xlsx"),))
        excel.load_a_workbook(excel_file_path)



    verify_existing = input(
        "Do want to verify existing numbers or fetch new ones?\n1. Verify existing\n2. Fetch "
        "new\nInput 1 or 2: "
    )
    if verify_existing == "1":
        excel2 = ExcelBot()
        excel_file_path = filedialog.askopenfilename(
            title="Select Excel file with numbers", filetypes=(("Excel files", "*.xlsx"),)
        )
        excel2.load_a_workbook(excel_file_path)
        verify_mode = 1
    elif verify_existing == "2":
        verify_mode = 2
    else:
        messagebox.showerror("Error", "Invalid input")

bot = WhatsAppBot()
bot.verification_mode = verify_mode

if verify_mode == 1:
    bot.number_list_to_verify = excel2.get_first_column_elements()
    print(f"Total numbers to verify: {len(bot.number_list_to_verify)}")
elif verify_mode == 2:
    start_number = int(input("Enter the starting number (with country code): "))  # 447947030019
    total_numbers = int(input("Enter the total amount of numbers: "))  # 100
    num_list = list(range(start_number, start_number + total_numbers))
    # convert every number to string
    num_list = [str(num) for num in num_list]
    random.shuffle(num_list)
    bot.total_numbers = total_numbers
    with open("numbers.txt", "w") as f:
        for num in num_list:
            f.write(str(num) + "\n") if num != num_list[-1] else f.write(str(num))
    bot.number_list_to_verify = num_list
elif verify_mode == 3:
    bot.total_numbers = len(number_list_to_verify)
    bot.number_list_to_verify = number_list_to_verify


bot.start()
bot.goto_whatsapp()
bot.goto_new_chat()
bot.start_getting_numbers(excel)
bot.quit()
messagebox.showinfo("Fetching Done", f"Total numbers found: {bot.existing_numbers}")

# Terminal command to convert my project to exe using pyinstaller:
# pyinstaller --onefile bot.py

