"""
This scripts validates an Excel file with a given schema and convert valid data into XML file
"""
# pylint: disable=C0103

from __future__ import print_function
import sys
import argparse
from XLSReader import XLSReader
import utils

arg_parser = argparse.ArgumentParser(
    description='Transform and output validated data from an excel file to a XML file')
arg_parser.add_argument('xls', help='Excel file to be validated and transformed')
arg_parser.add_argument('xml', help='XML file to be written to')
arg_parser.add_argument('--conf', required=True, dest='conf',
                        help='Configuration file contains list of worksheets and fields')
arg_parser.add_argument('--conf-key', required=True, dest='confKey',
                        help='Keys/tabs (comma delimited) to retrieve the list of field')
arg_parser.add_argument('--schema', required=True, dest='schema',
                        help='Schema definition for data field')
arg_parser.add_argument('--xslt', required=True, dest='xslt',
                        help='Definition for transformation from xls to xml document')

args = arg_parser.parse_args()
xls_filename = args.xls
xml_filename = args.xml
xls_conf = args.conf
xls_conf_keys = args.confKey.split(',')
xls_schema = args.schema
xslt_filename = args.xslt

xls_reader = XLSReader(xls_filename, xls_conf)
xls_readers = { key : xls_reader for key in xls_conf_keys }

try:
    output_xml = utils.multiple_objects_to_xml(xls_readers, xls_schema, xslt_filename)
except Exception as e:
    print(e.message, file=sys.stderr)
    quit(1)

with open(xml_filename, 'w') as xml_file:
    utils.save_xml(output_xml, xml_file)

print('Conversion complete!', file=sys.stdout)
