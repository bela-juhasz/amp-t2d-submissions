"""
This scripts validates a TSV file with a given schema and convert valid data into XML file
"""
# pylint: disable=C0103
import re
import argparse
from lxml import etree
from TSVReader import TSVReader
from MetadataValidator import MetadataValidator

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
tsv_validator = MetadataValidator(tsv_schema)

if not tsv_reader.is_valid():
    print 'TSV file does not contain required fields!'
    quit()

headers = tsv_reader.get_headers()
input_xml_root = etree.Element(tsv_conf_key+"Set")
row = tsv_reader.next_row()
while row:
    if tsv_validator.validate_data(row, tsv_conf_key):
        element_root = etree.SubElement(input_xml_root, tsv_conf_key)
        for header in headers:
            # must start with a letter or underscore
            tag_name = re.sub('^[^a-zA-Z_]+', '_', header)
            # contain only letters, digits, hyphens, underscores and periods
            tag_name = re.sub('[^-0-9a-zA-Z_.]', '_', tag_name)
            child_node = etree.SubElement(element_root, tag_name)
            child_node.text = str(row[header])
    else:
        print 'Please fix above error at file ' + tsv_filename + '!'
    row = tsv_reader.next_row()

xslt_tree = etree.parse(xslt_filename)
transform = etree.XSLT(xslt_tree)
output_xml = transform(input_xml_root)

with open(xml_filename, 'w') as xml_file:
    xml_file.write(etree.tostring(output_xml, pretty_print=True))

print 'Conversion complete!'
