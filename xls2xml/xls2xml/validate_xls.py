"""
This script validates an excel file with a given schema
"""
# pylint: disable=C0103

from __future__ import print_function
import sys
import argparse
from XLSReader import XLSReader
from utils import validate_file

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
has_no_error = validate_file(xls_reader, xls_schema)

if not has_no_error:
    print('Validation failed!', file=sys.stderr)
    quit(1)

print('Validation completed!', file=sys.stdout)
