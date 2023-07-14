from RPA.Excel.Files import Files


class Excel_RPA:
    def __init__(self):
        self.excel_file = Files()

    def save_collection(self, name, collection):
        # Create a new Excel file
        self.excel_file.create_workbook(name)
        self.write_collection(collection)
        self.excel_file.save_workbook()
        self.excel_file.close_workbook()
        return True

    def write_collection(self, collection):
        # Set the headers
        headers = [list(collection[0].keys())]
        data_values = [list(d.values()) for d in collection]

        self.excel_file.set_cell_values("A1", headers)
        self.excel_file.set_cell_values("A2", data_values)