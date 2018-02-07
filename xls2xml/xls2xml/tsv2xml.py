"""
This scripts validates a TSV file with a given schema and convert valid data into XML file
"""
# pylint: disable=C0103
# pylint: disable=relative-import

from __future__ import print_function
import sys
import argparse
from TSVReader import TSVReader
import utils

arg_parser = argparse.ArgumentParser(
    description='Transform and output validated data from an TSV file to a XML file')
arg_parser.add_argument('tsv', help='TSV file to be validated and transformed')
arg_parser.add_argument('xml', help='XML file to be written to')
arg_parser.add_argument('--conf', required=True, dest='conf',
                        help='Configuration file contains list of fields to be parsed')
arg_parser.add_argument('--conf-key', required=True, dest='confKey',
                        help='Key to retrieve the list of field')
arg_parser.add_argument('--schema', required=True, dest='schema',
                        help='Schema definition for data field')
arg_parser.add_argument('--xslt', required=True, dest='xslt',
                        help='Definition for transformation from tsv to xml document')

args = arg_parser.parse_args()
tsv_filename = args.tsv
xml_filename = args.xml
tsv_conf = args.conf
tsv_conf_key = args.confKey
tsv_schema = args.schema
xslt_filename = args.xslt

tsv_reader = TSVReader(tsv_filename, tsv_conf, tsv_conf_key)
rows = []
has_validation_error = utils.extract_rows(tsv_reader, tsv_conf_key, tsv_schema, rows)
if has_validation_error:
    quit(1)

input_xml_root = utils.rows_to_xml(rows, tsv_conf_key)
output_xml = utils.transform_xml(input_xml_root, xslt_filename)

with open(xml_filename, 'w') as xml_file:
    utils.save_xml(output_xml, xml_file)

print('Conversion complete!', file=sys.stdout)
