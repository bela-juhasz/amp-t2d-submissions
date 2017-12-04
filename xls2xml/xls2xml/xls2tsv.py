"""
This scripts validates an Excel file with a given schema and convert valid data into TSV file
"""
# pylint: disable=C0103
import argparse
import tsv
from XLSReader import XLSReader
from MetadataValidator import MetadataValidator

arg_parser = argparse.ArgumentParser(
    description='Transform and output validated data from an excel file to a TSV file')
arg_parser.add_argument('xls', help='Excel file to be validated and transformed')
arg_parser.add_argument('tsv', help='TSV file to be written to')
arg_parser.add_argument('--conf', required=True, dest='conf',
                        help='Configuration file containing list of worksheets and fields')
arg_parser.add_argument('--conf-key', required=True, dest='confKey',
                        help='Key to retrieve the list of field')
arg_parser.add_argument('--schema', required=True, dest='schema',
                        help='Schema definition for data field')

args = arg_parser.parse_args()
xls_filename = args.xls
tsv_filename = args.tsv
xls_conf = args.conf
xls_conf_key = args.confKey
xls_schema = args.schema

xls_reader = XLSReader(xls_filename, xls_conf)

headers = xls_reader.get_headers_by_worksheet(xls_conf_key)
if not headers:
    quit()

tsv_writer = tsv.TsvWriter(open(tsv_filename, 'w'))
tsv_writer.list_line(headers)

xls_validator = MetadataValidator(xls_schema)
xls_reader.active = xls_conf_key
for row in xls_reader:
    if xls_validator.validate_data(row, xls_conf_key):
        values = [ '' if row[header] is None else row[header] for header in headers ]
        tsv_writer.list_line(values)
    else:
        print 'Please fix above error at worksheet '+xls_conf_key+', row '+str(row['row_num'])+'!'

tsv_writer.close()

print 'Conversion complete!'
