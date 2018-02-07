"""
This script validates a TSV file with a given schema
"""
# pylint: disable=C0103

from __future__ import print_function
import sys
import argparse
from TSVReader import TSVReader
from utils import validate_file

arg_parser = argparse.ArgumentParser(description='Validate data from a TSV file')
arg_parser.add_argument('tsv', help='TSV file to be validated')
arg_parser.add_argument('--conf', required=True, dest='conf',
                        help='Configuration file contains list of fields to be parsed')
arg_parser.add_argument('--conf-key', required=True, dest='confKey',
                        help='Key to retrieve the list of fields in a configuration file')
arg_parser.add_argument('--schema', required=True, dest='schema',
                        help='Schema definition for data field')

args = arg_parser.parse_args()
tsv_filename = args.tsv
tsv_conf = args.conf
tsv_conf_key = args.confKey
tsv_schema = args.schema

tsv_reader = TSVReader(tsv_filename, tsv_conf, tsv_conf_key)
if not tsv_reader.is_valid():
    print('TSV file does not have all the required fields!', file=sys.stderr)
    print('Validation failed!', file=sys.stderr)
    quit(1)

has_no_error = validate_file(tsv_reader, tsv_schema)
if not has_no_error:
    print('Validation failed!', file=sys.stderr)
    quit(1)

print('Validation completed!', file=sys.stdout)
