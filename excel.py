from openpyexcel import load_workbook, Workbook


class ExcelBot:
    def __init__(self):
        self.wb = None
        self.ws = None
        self.excel_file_path = ""
        self.number_list_to_verify = []

    def create_workbook(self, folder, file_name):
        self.excel_file_path = f"{folder}/{file_name}.xlsx"
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["Number", "Status"])
        self.wb.save(self.excel_file_path)

    def load_a_workbook(self, file_path):
        self.excel_file_path = file_path
        self.wb = load_workbook(self.excel_file_path)
        self.ws = self.wb.active

    def write_to_workbook(self, *args):
        self.ws.append([*args])
        self.wb.save(self.excel_file_path)

    def save_workbook(self):
        self.wb.save(self.excel_file_path)

    def get_first_column_elements(self):
        return [cell.value for cell in self.ws['A']]
