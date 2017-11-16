from openpyxl import load_workbook
import yaml

worksheets_key_name = 'worksheets'
required_headers_key_name = 'required'
optional_headers_key_name = 'optional'

class XLSReader():
    def __init__(self, xls_filename, conf_filename):
        with open(conf_filename, 'r') as conf_file:
            self.xls_conf = yaml.load(conf_file)
        self.workbook = load_workbook(xls_filename, read_only=True)
        self.worksheets = None
        self.row_offset = {}
        self.headers = {}

    def valid_worksheets(self):
        if self.worksheets is not None:
            return self.worksheets

        self.worksheets = []
        sheet_titles = self.workbook.sheetnames
        for title in self.xls_conf[worksheets_key_name]:
            # Check worksheet exists
            if title not in sheet_titles:
                continue

            # Check number of rows
            worksheet = self.workbook[title]
            num_rows = 0
            for row in worksheet.rows:
                num_rows += 1
            if num_rows < 2:
                continue

            # Check required headers are present
            if title not in self.headers:
                self.headers[title] = []
            for cell in worksheet[1]:
                header_value = cell.value
                if header_value is None:
                    self.headers[title].append(header_value)
                else:
                    self.headers[title].append(header_value.strip())
            required_headers = self.xls_conf[title][required_headers_key_name]
            required_header_not_found = False
            for required_header in required_headers:
                if required_header not in self.headers[title]:
                    required_header_not_found = True
                    break
            if required_header_not_found:
                continue

            self.worksheets.append(title)

        return self.worksheets

    def get_headers_by_worksheet(self, worksheet):
        worksheets = self.valid_worksheets()
        if worksheet not in worksheets:
            print('Worksheet '+worksheet+' is not available or not valid!')
            return []

        return [ x for x in self.headers[worksheet] if x is not None ]


    def next_row(self, sheet_name):
        if self.worksheets is None:
            self.valid_worksheets()

        if sheet_name not in self.worksheets:
            print('Worksheet ' + sheet_name + ' is not valid!')
            return False

        if sheet_name not in self.row_offset:
            self.row_offset[sheet_name] = 1
        self.row_offset[sheet_name] += 1

        worksheet = self.workbook[sheet_name]
        required_headers = self.xls_conf[sheet_name][required_headers_key_name]
        optional_headers = self.xls_conf[sheet_name][optional_headers_key_name]

        for row in worksheet.iter_rows(min_row=self.row_offset[sheet_name]):
            num_cells = 0
            for cell in row:
                num_cells += 1

            data = {}
            go_to_next_row = False
            has_notnull = False
            for header in required_headers+optional_headers:
                header_index = self.headers[sheet_name].index(header)
                if header_index >= num_cells:
                    go_to_next_row = True
                    break

                cell = row[header_index]
                if cell.value is not None:
                    has_notnull = True

                if type(cell.value) is unicode:
                    data[header] = cell.value.encode('ascii','ignore')
                else:
                    data[header] = cell.value

            if go_to_next_row or not has_notnull:
                self.row_offset[sheet_name] += 1
                continue

            data['row_num'] = self.row_offset[sheet_name];
            return data

        return False
