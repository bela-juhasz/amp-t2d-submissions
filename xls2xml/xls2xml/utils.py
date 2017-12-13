import re

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
