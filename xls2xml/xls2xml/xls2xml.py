"""
This scripts validates an Excel file with a given schema and convert valid data into XML file
"""
# pylint: disable=C0103
import re
import argparse
from lxml import etree
from XLSReader import XLSReader
from MetadataValidator import MetadataValidator

arg_parser = argparse.ArgumentParser(
    description='Transform and output validated data from an excel file to a XML file')
arg_parser.add_argument('xls', help='Excel file to be validated and transformed')
arg_parser.add_argument('xml', help='XML file to be written to')
arg_parser.add_argument('--conf', required=True, dest='conf',
                        help='Configuration file contains list of worksheets and fields')
arg_parser.add_argument('--conf-key', required=True, dest='confKey',
                        help='Key to retrieve the list of field')
arg_parser.add_argument('--schema', required=True, dest='schema',
                        help='Schema definition for data field')
arg_parser.add_argument('--xslt', required=True, dest='xslt',
                        help='Definition for transformation from xls to xml document')

args = arg_parser.parse_args()
xls_filename = args.xls
xml_filename = args.xml
xls_conf = args.conf
xls_conf_key = args.confKey
xls_schema = args.schema
xslt_filename = args.xslt

xls_reader = XLSReader(xls_filename, xls_conf)

headers = xls_reader.get_headers_by_worksheet(xls_conf_key)
if not headers:
    quit()

xls_validator = MetadataValidator(xls_schema)

input_xml_root = etree.Element(xls_conf_key+"Set")
row = xls_reader.next_row(xls_conf_key)
while row:
    if xls_validator.validate_data(row, xls_conf_key):
        element_root = etree.SubElement(input_xml_root, xls_conf_key)
        for header in headers:
            # must start with a letter or underscore
            tag_name = re.sub('^[^a-zA-Z_]+', '_', header)
            # contain only letters, digits, hyphens, underscores and periods
            tag_name = re.sub('[^-0-9a-zA-Z_.]', '_', tag_name)
            child_node = etree.SubElement(element_root, tag_name)
            child_node.text = str(row[header])
    else:
        print("Please fix above error at worksheet " + xls_conf_key + ", row "
              + str(row["row_num"]) + "!")
    row = xls_reader.next_row(xls_conf_key)

xslt_tree = etree.parse(xslt_filename)
transform = etree.XSLT(xslt_tree)
output_xml = transform(input_xml_root)

with open(xml_filename, 'w') as xml_file:
    xml_file.write(etree.tostring(output_xml, pretty_print=True))

print 'Conversion complete!'
