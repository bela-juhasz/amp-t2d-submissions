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
    epilog='Please put "--conf-key" arguments and their corresponding "tsv" file names in the same order!',
    description='Transform and output validated data from one or more TSV files to a XML file')
arg_parser.add_argument('tsv', help='TSV files (comma delimited) to be validated and transformed')
arg_parser.add_argument('xml', help='XML file to be written to')
arg_parser.add_argument('--conf', required=True, dest='conf',
                        help='Configuration file contains list of fields to be parsed')
arg_parser.add_argument('--conf-key', required=True, dest='confKey',
                        help='Keys (comma delimited) to retrieve the list of field')
arg_parser.add_argument('--schema', required=True, dest='schema',
                        help='Schema definition for data field')
arg_parser.add_argument('--xslt', required=True, dest='xslt',
                        help='Definition for transformation from tsv to xml document')

args = arg_parser.parse_args()
tsv_filenames = args.tsv.split(',')
xml_filename = args.xml
tsv_conf = args.conf
tsv_conf_keys = args.confKey.split(',')
tsv_schema = args.schema
xslt_filename = args.xslt

key_files = dict(zip(tsv_conf_keys, tsv_filenames))
tsv_readers = [ (key, TSVReader(key_files[key], tsv_conf, key)) for key in key_files ]

try:
    output_xml = utils.multiple_objects_to_xml(tsv_readers, tsv_schema, xslt_filename)
except Exception as e:
    print(e.message, file=sys.stderr)
    quit(1)

with open(xml_filename, 'w') as xml_file:
    utils.save_xml(output_xml, xml_file)

print('Conversion complete!', file=sys.stdout)
