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
        headers = list(collection[0].keys())
        # Write the headers to the worksheet
        for col, header in enumerate(headers, start=1):
            self.excel_file.set_cell_value(row=1, column=col, value=header)

        # Writing to the worksheet
        for row, news in enumerate(collection, start=2):
            for col, value in enumerate(news.values(), start=1):
                self.excel_file.set_cell_value(row=row, column=col, value=value)
