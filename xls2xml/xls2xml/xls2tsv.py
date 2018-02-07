"""
This scripts validates an Excel file with a given schema and convert valid data into TSV file
"""
# pylint: disable=C0103

from __future__ import print_function
import sys
import argparse
import tsv
from XLSReader import XLSReader
import utils

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
rows = []
has_no_error = utils.extract_rows(xls_reader, xls_conf_key, xls_schema, rows)
if not has_no_error:
    quit(1)

tsv_writer = tsv.TsvWriter(open(tsv_filename, 'w'))

xls_reader.set_current_conf_key(xls_conf_key)
headers = xls_reader.get_current_headers()
tsv_writer.list_line(headers)

for row in rows:
    values = ['' if row.get(header) is None else row.get(header) for header in headers]
    tsv_writer.list_line(values)

tsv_writer.close()

print('Conversion complete!', file=sys.stdout)
