from time import sleep
from bot import WhatsAppBot
from excel import ExcelBot
from tkinter import filedialog, messagebox
import winsound

excel = ExcelBot()
verify_mode = 1

create_sheet = input("Type 'y' to create a new sheet or any other key to select an existing one: ")
if create_sheet == "y":
    folder = filedialog.askdirectory(title="Select folder to save file")
    file_name = input("Enter file name: ")
    excel.create_workbook(folder, file_name)
else:
    excel_file_path = filedialog.askopenfilename(title="Select Excel file", filetypes=(("Excel files", "*.xlsx"),))
    excel.load_a_workbook(excel_file_path)

verify_existing = input(
    "Do want to verify existing numbers or fetch new ones?\n1. Verify existing\n2. Fetch "
    "new\nInput 1 or 2: "
)
if verify_existing == "1":
    excel_file_path = filedialog.askopenfilename(
        title="Select Excel file with numbers", filetypes=(("Excel files", "*.xlsx"),)
    )
    excel.load_a_workbook(excel_file_path)
    verify_mode = 1
elif verify_existing == "2":
    verify_mode = 2
else:
    messagebox.showerror("Error", "Invalid input")

bot = WhatsAppBot()
bot.verification_mode = verify_mode

if verify_mode == 1:
    bot.number_list_to_verify = excel.get_first_column_elements()
    print(f"Total numbers to verify: {len(bot.number_list_to_verify)}")
elif verify_mode == 2:
    bot.start_number = int(input("Enter the starting number (with country code): "))  # 447947030019
    bot.total_numbers = int(input("Enter the total amount of numbers: "))  # 100

bot.start()
bot.goto_whatsapp()
bot.goto_new_chat()
bot.start_getting_numbers(excel)
bot.quit()
messagebox.showinfo("Fetching Done", f"Total numbers found: {bot.existing_numbers}")
