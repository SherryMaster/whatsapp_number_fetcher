from time import sleep
from bot import WhatsAppBot
from excel import ExcelBot
from tkinter import filedialog

create_sheet = input("Type 'y' to create a new sheet or any other key to select an existing one: ")
if create_sheet == "y":
    folder = filedialog.askdirectory(title="Select folder to save file")
    file_name = input("Enter file name: ")
    excel = ExcelBot()
    excel.create_workbook(folder, file_name)
else:
    excel_file_path = filedialog.askopenfilename(title="Select Excel file", filetypes=(("Excel files", "*.xlsx"),))
    excel = ExcelBot()
    excel.load_a_workbook(excel_file_path)


bot = WhatsAppBot()

bot.start_number = int(input("Enter the starting number (with country code): "))
bot.total_numbers = int(input("Enter the total amount of numbers: "))

bot.start()
bot.goto_whatsapp()
bot.goto_new_chat()
bot.start_getting_numbers(excel)
bot.quit()