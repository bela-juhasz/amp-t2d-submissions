from __future__ import print_function
import sys
import re
from lxml import etree
from MetadataValidator import MetadataValidator

def header_to_xml_tag(header):
    """
    Convert an header to XML specification compliant tag name
    :param header: header string to be converted
    :type header: basestring
    :return: converted string with any illegal chars replaced with underscores
    :rtype: basestring
    """
    # are case-sensitive
    tag = header
    # cannot start with the letters xml (or XML, or Xml, etc)
    tag = re.sub('^xml', '_', tag, flags=re.IGNORECASE)
    # must start with a letter or underscore
    tag = re.sub('^[^a-zA-Z_]+', '_', tag)
    # contain only letters, digits, hyphens, underscores and periods
    tag = re.sub('[^-0-9a-zA-Z_.]', '_', tag)
    # cannot contain spaces (same as above)

    return tag

def validate_file(reader, validation_schema_filename):
    """
    Validate a data file (XLS or TSV)

    :param reader: reader for the file (XLS or TSV)
    :type reader: Reader
    :param validation_schema_filename: path to validation rules definition file
    :type validation_schema_filename: basestring
    :return: False if there is error or True for success
    :rtype: bool
    """
    has_validation_error = False
    validator = MetadataValidator(validation_schema_filename)
    keys = reader.get_valid_conf_keys()
    for key in keys:
        reader.set_current_conf_key(key)
        for row in reader:
            if not validator.validate_data(row, key):
                has_validation_error = True

    return not has_validation_error


def extract_rows(reader, current_key, validation_schema_filename, rows):
    """
    Extract data from a XLS worksheet or TSV file named $current_key

    :param reader: reader for the file (XLS or TSV)
    :type reader: Reader
    :param current_key: the key name defined in the configuration file
    :type current_key: basestring
    :param validation_schema_filename: path to validation rules definition file
    :type validation_schema_filename:  basestring
    :param rows: list to append the valid data rows
    :type rows: list
    :return: False if there is error or True for success
    :rtype: bool
    """
    reader.set_current_conf_key(current_key)
    try:
        headers = reader.get_current_headers()
    except Exception as e:
        print(e.message, file=sys.stderr)
        return False
    if not headers:
        print('There is no header row!', file=sys.stderr)
        return False

    has_validation_error = False
    validator = MetadataValidator(validation_schema_filename)

    for row in reader:
        if validator.validate_data(row, current_key):
            rows.append(row)
        else:
            has_validation_error = True

    if has_validation_error:
        print("Please fix error first!", file=sys.stderr)
        return False

    return True

def rows_to_xml(rows, current_key):
    """
    Convert data in a list of mappings into an xml tree

    :param rows: a list of mappings
    :type rows: list
    :param current_key: a string to indicate which metadata set this is (e.g. Sample)
    :type current_key: basestring
    :return: xml tree
    :rtype: etree.Element
    """
    xml = etree.Element(current_key+"Set")
    for row in rows:
        element_root = etree.SubElement(xml, current_key)
        for header in row:
            child_node = etree.SubElement(element_root, header_to_xml_tag(header))
            child_node.text = str('' if row.get(header, '') is None else row.get(header, ''))
    return xml

def transform_xml(input_xml, xslt_filename):
    """
    Transform a xml tree to another according to the xslt transformation rules defined in
    $xslt_filename

    :param input_xml: the input xml tree
    :type input_xml: etree._Element
    :param xslt_filename: path to the definition file of xslt transformation rules
    :type xslt_filename: basestring
    :return: the transformed xml tree
    :rtype: etree.Element
    """
    xslt_tree = etree.parse(xslt_filename)
    transform = etree.XSLT(xslt_tree)
    output_xml = transform(input_xml)

    if transform.error_log:
        print('Errors during XSLT transformation: {}'.format(transform.error_log))

    return output_xml

def save_xml(input_xml, outfile):
    """
    Save the contents of an xml tree and write them to a file handle

    :param input_xml: the input xml tree
    :type input_xml: etree._Element
    :param outfile: output file handle
    :type outfile: File
    """
    outfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    if input_xml.getroot() is not None:
        # The original method to serialize XML (i.e. etree.tostring)
        # couldn't handle non-well-formed XML:
        outfile.write(etree.tostring(input_xml, pretty_print=True))
        # TODO bjuhasz: write a test for this, demonstrating it
        #outfile.write(unicode(input_xml))

def multiple_objects_to_xml(input_readers, xls_schema_filename, xslt_filename):
    """
    Retrieve data from multiple objects and transform into an xml tree

    :param input_readers: XLS or TSV file readers in [ (conf_key, file_reader) ] form
    :type xls_reader: list of tuples
    :param xls_schema_filename: path to the validation rules definition file
    :type xls_schema_filename: basestring
    :param xslt_filename: path to the xslt transformation rules definition
    :type xslt_filename: basestring
    :return: transformed xml tree object
    :rtype: etree.Element
    """
    input_xml_root = etree.Element("ResultSet")
    for reader in input_readers:
        rows = []
        key = reader[0]
        if extract_rows(reader[1], key, xls_schema_filename, rows):
            input_xml_root.append(rows_to_xml(rows, key))
        else:
            raise Exception('Failed to extract data for worksheet ' + key)

    output_xml = transform_xml(input_xml_root, xslt_filename)
    return output_xml
