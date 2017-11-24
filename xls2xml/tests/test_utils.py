from xls2xml import header_to_xml_tag

def test_header_to_xml_tag():
    # are case-sensitive
    assert 'This_is_XML_tag' == header_to_xml_tag('This_is_XML_tag')
    # cannot start with the letters xml (or XML, or Xml, etc)
    assert '__tag' == header_to_xml_tag('XML_tag')
    assert '__tag' == header_to_xml_tag('Xml_tag')
    assert '__tag' == header_to_xml_tag('xml_tag')
    assert '_xml_tag' == header_to_xml_tag('_xml_tag')
    # must start with a letter or underscore
    assert 'first_XML_tag' == header_to_xml_tag('first_XML_tag')
    assert '_first_XML_tag' == header_to_xml_tag('_first_XML_tag')
    assert '_st_XML_tag' == header_to_xml_tag('1st_XML_tag')
    # contain only letters, digits, hyphens, underscores and periods
    assert 'this_one_XML_tag' == header_to_xml_tag('this_one_XML_tag')
    assert 'this_1_XML_tag' == header_to_xml_tag('this_1_XML_tag')
    assert 'this-one-XML-tag' == header_to_xml_tag('this-one-XML-tag')
    assert 'this_1.0_XML_tag' == header_to_xml_tag('this_1.0_XML_tag')
    assert 'this_____________________________XML_tag' ==\
           header_to_xml_tag('this_!@#$%^&*()+={}[]:;|\/?<>,~`_XML_tag')
    # cannot contain spaces
    assert '_this_XML_tag_' == header_to_xml_tag(' this XML tag ')
