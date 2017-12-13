"""
This module reads a TSV file and allows the user to get the 1st line and iterate over the
rest of the file row by row (next_row()). The returned row is a hash which contains only
the keys that are defined in a configuration file.

This module depends on tsv and pyyaml.
"""

from tsv import TsvReader
import yaml

REQUIRED_HEADERS_KEY_NAME = 'required'
OPTIONAL_HEADERS_KEY_NAME = 'optional'
DATA_TYPE_KEY_NAME = 'data_type'
DATA_TYPE_TO_FUNCTION = {
    'int':      int,
    'float':    float,
    'long':     long,
    'str':      str
}

class TSVReader(object):
    """
    Reader for TSV file for the fields from a configuration file
    """

    def __init__(self, tsv_filename, conf_filename, conf_key):
        """
        Constructor

        :param tsv_filename: TSV file path
        :type tsv_filename: basestring
        :param conf_filename: configuration file path
        :type conf_filename: basestring
        :param conf_key: first level key in the configuration to access that section
        :type conf_key: basestring
        """
        with open(conf_filename, 'r') as conf_file:
            self.tsv_conf = yaml.load(conf_file)
            self.tsv_conf_key = conf_key
        self.tsv_reader = TsvReader(open(tsv_filename, 'r'))
        self.tsv_iterator = iter(self.tsv_reader)
        self.headers = self.tsv_iterator.next()
        self.valid = None

    def __del__(self):
        self.tsv_reader.close()

    def __iter__(self):
        return self

    def is_valid(self):
        """
        Check if the TSV file has all the REQUIRED fields defined in the configuration file

        :return: True if all the REQUIRED fields are present
        :rtype: bool
        """
        if self.valid is not None:
            return self.valid

        required_headers = self.tsv_conf[self.tsv_conf_key].get(REQUIRED_HEADERS_KEY_NAME, [])
        self.valid = set(required_headers) <= set(self.headers) # issubset

        return self.valid

    def get_headers(self):
        """
        :return: The list of field names in the first line of the TSV file.
        :rtype: list
        """
        return self.headers

    def next(self):
        """
        Retrieve next data row

        :return: A hash containing all the REQUIRED and OPTIONAL fields as keys
                and the corresponding data as values.
        :rtype: dict
        """
        if not self.is_valid():
            raise StopIteration

        this_row = self.tsv_iterator.next()

        data = {}
        num_cells = len(this_row)
        has_notnull = False
        required_headers = self.tsv_conf[self.tsv_conf_key].get(REQUIRED_HEADERS_KEY_NAME, [])
        optional_headers = self.tsv_conf[self.tsv_conf_key].get(OPTIONAL_HEADERS_KEY_NAME, [])
        data_type = self.tsv_conf[self.tsv_conf_key].get(DATA_TYPE_KEY_NAME, {})
        for header in required_headers+optional_headers:
            cell = ''

            header_index = num_cells
            if header in self.headers:
                header_index = self.headers.index(header)
            if header_index < num_cells:
                cell = this_row[header_index]
                if cell is not None:
                    has_notnull = True

            if not cell:
                data[header] = None
            elif header in data_type:
                data[header] = DATA_TYPE_TO_FUNCTION[data_type[header]](cell)
            else:
                data[header] = cell

        if has_notnull:
            return data

        # no data on this row, continue to next
        return self.next()
