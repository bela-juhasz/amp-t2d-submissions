from tsv import TsvReader
import yaml

required_headers_key_name = 'required'
optional_headers_key_name = 'optional'

class TSVReader():
    def __init__(self, tsv_filename, conf_filename, conf_key):
        with open(conf_filename, 'r') as conf_file:
            self.tsv_conf = yaml.load(conf_file)
            self.tsv_conf_key = conf_key
            self.required_headers = self.tsv_conf[self.tsv_conf_key][required_headers_key_name]
            self.optional_headers = self.tsv_conf[self.tsv_conf_key][optional_headers_key_name]
        self.tsv_reader = TsvReader(open(tsv_filename, 'r'))
        self.tsv_iterator = iter(self.tsv_reader)
        self.headers = self.tsv_iterator.next()
        self.valid = None

    def __del__(self):
        self.tsv_reader.close()

    def isValid(self):
        if self.valid is not None:
            return self.valid

        self.valid = True
        required_headers = self.tsv_conf[self.tsv_conf_key][required_headers_key_name]
        for required_header in required_headers:
            if required_header not in self.headers:
                self.valid = False
                break

        return self.valid

    def get_headers(self):
        return self.headers

    def next_row(self):
        data = {}

        if not self.isValid():
            return data

        try:
            this_row = self.tsv_iterator.next()
        except StopIteration:
            this_row = False

        if not this_row:
            return data

        num_cells = len(this_row)
        has_notnull = False
        for header in self.required_headers+self.optional_headers:
            cell = ''

            header_index = self.headers.index(header)
            if header_index < num_cells:
                cell = this_row[header_index]
                if cell is not None:
                    has_notnull = True

            if type(cell) is unicode:
                data[header] = cell.encode('ascii','ignore')
            else:
                data[header] = cell

        if not has_notnull:
            return self.next_row()

        return data
