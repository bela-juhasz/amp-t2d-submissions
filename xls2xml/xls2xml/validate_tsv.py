"""
This script validates a TSV file with a given schema
"""
# pylint: disable=C0103
import argparse
from TSVReader import TSVReader
from MetadataValidator import MetadataValidator

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
tsv_validator = MetadataValidator(tsv_schema)

if not tsv_reader.is_valid():
    print 'TSV file does not contain required fields!'
    quit()

has_error = False
for row in tsv_reader:
    if not tsv_validator.validate_data(row, tsv_conf_key):
        has_error = True

if has_error:
    print 'Please fix above error at file ' + tsv_filename + '!'
else:
    print 'Validation completed!'
