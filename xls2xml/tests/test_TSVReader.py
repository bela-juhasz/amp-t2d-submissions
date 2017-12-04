from xls2xml import TSVReader

def test_is_not_valid():
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v1.conf', 'Analysis')
    assert not tsv_reader.is_valid()

def test_is_valid():
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v1.conf', 'Sample')
    assert tsv_reader.is_valid()

def test_get_headers():
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v1.conf', 'Sample')
    headers = tsv_reader.get_headers()
    assert isinstance(headers, list)
    assert set(headers) == {'Sample_ID', 'Subject_ID', 'Geno_ID', 'Phenotype', 'Gender', 'Analysis_alias', 'Cohort ID',
                            'Ethnicity', 'Ethnicity Description', 'T2D', 'Case_Control', 'Description', 'Center_name',
                            'Hispanic or Latino; of Spanish origin', 'Age', 'Year of Birth', 'Year of first visit',
                            'Cell Type', 'Maternal_id', 'Paternal_id', 'Novel Attributes'}

def test_next_row():
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v1.conf', 'Sample')
    row = tsv_reader.next()
    assert isinstance(row, dict)
    assert 0 == cmp(row, {'Novel Attributes': '', 'Ethnicity Description': '', 'Description': 'Male normal',
                          'Cell Type': 'Blood', 'Maternal_id': 'SAM111113', 'Center_name': 'WTGC cambridge',
                          'Gender': 'male', 'Subject_ID': 'SAM111111', 'Paternal_id': 'SAM111115', 'T2D': '0',
                          'Hispanic or Latino; of Spanish origin': '', 'Cohort ID': 'CO1111', 'Year of Birth': '1986',
                          'Age': '31', 'Analysis_alias': 'AN001', 'Sample_ID': 'SAM111111', 'Geno_ID': '',
                          'Year of first visit': '', 'Case_Control': 'Control', 'Ethnicity': 'EUWH',
                          'Phenotype': 'MeSH:D006262'})
