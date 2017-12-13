"""
This script validates an excel file with a given schema
"""
# pylint: disable=C0103

from __future__ import print_function
import sys
import argparse
from XLSReader import XLSReader
from MetadataValidator import MetadataValidator

arg_parser = argparse.ArgumentParser(description='Validate data from an excel file')
arg_parser.add_argument('xls', help='Excel file to be validated')
arg_parser.add_argument('--conf', required=True, dest='conf',
                        help='Configuration file containing list of worksheets and fields')
arg_parser.add_argument('--schema', required=True, dest='schema',
                        help='Schema definition for data field')

args = arg_parser.parse_args()
xls_filename = args.xls
xls_conf = args.conf
xls_schema = args.schema

xls_reader = XLSReader(xls_filename, xls_conf)
xls_validator = MetadataValidator(xls_schema)

worksheets = xls_reader.valid_worksheets()

if not worksheets:
    print('There is nothing to be validated', file=sys.stderr)
    quit(1)

has_validation_error = False
for ws in worksheets:
    xls_reader.active = ws
    for row in xls_reader:
        if not xls_validator.validate_data(row, ws):
            has_validation_error = True
            print('Please fix above error at worksheet '+ws+', row '+str(row['row_num'])+'!',
                  file=sys.stderr)

if has_validation_error:
    quit(1)

print('Validation completed!', file=sys.stdout)
