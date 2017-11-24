from xls2xml import MetadataValidator
from xls2xml import XLSReader
from xls2xml import TSVReader

def test_validate_data():
    validator = MetadataValidator('data/T2D_xls2xml_v1.schema')
    reader = XLSReader('data/example_AMP_T2D_Submission_form_V2.xlsx', 'data/T2D_xls2xml_v1.conf')
    reader.active = 'Sample'
    row = reader.next()
    assert validator.validate_data(row, 'Sample')
    reader.active = 'Analysis'
    row = reader.next()
    assert validator.validate_data(row, 'Analysis')
    reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v1.conf', 'Sample')
    row = reader.next()
    assert validator.validate_data(row, 'Sample')
