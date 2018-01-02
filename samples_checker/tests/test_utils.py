# pylint: disable=C0111
from samples_checker import utils

def test_get_samples_from_xml():
    samples = utils.get_samples_from_xml('data/T2D_Sample.xml')
    assert isinstance(samples, dict)
    assert samples == {'SAM111116': '', 'SAM111115': '', 'SAM111114': '', 'SAM111113': '',
                       'SAM111112': 'FEM1', 'SAM111111': ''}

def test_get_files_from_xml():
    files = utils.get_files_from_xml('data/T2D_File.xml')
    assert isinstance(files, dict)
    assert files == {'genotypes.4.vcf': 'vcf', 'genotypes.6.vcf': 'vcf',
                     'summary.hyperinsulinism.tsv': '', 'genotypes.8.vcf': 'vcf'}

def test_get_samples_from_vcf():
    samples = utils.get_samples_from_vcf('data/genotypes.4.vcf')
    assert isinstance(samples, list)
    assert samples == ['SAM111113', 'SAM111114', 'SAM111115', 'SAM111116']

def test_get_sample_ids():
    samples_in = {'SAM111116': '', 'SAM111115': '', 'SAM111114': '', 'SAM111113': '',
                  'SAM111112': 'FEM1', 'SAM111111': ''}
    samples_out = utils.get_sample_ids(samples_in)
    assert isinstance(samples_out, list)
    assert samples_out == ['SAM111116', 'SAM111115', 'SAM111114', 'SAM111113',
                           'SAM111112', 'SAM111111']

def test_get_genotype_ids():
    samples_in = {'SAM111116': '', 'SAM111115': '', 'SAM111114': '', 'SAM111113': '',
                  'SAM111112': 'FEM1', 'SAM111111': ''}
    samples_out = utils.get_genotype_ids(samples_in)
    assert isinstance(samples_out, list)
    assert samples_out == ['SAM111116', 'SAM111115', 'SAM111114', 'SAM111113',
                           'FEM1', 'SAM111111']

def test_check_samples_in_file():
    samples_in = {'SAM111116': '', 'SAM111115': '', 'SAM111114': '', 'SAM111113': '',
                  'SAM111112': 'FEM1', 'SAM111111': ''}
    difference = utils.check_samples_in_file(samples_in, 'data/genotypes.6.vcf', 'vcf')
    assert isinstance(difference, list)
    assert difference == ['SAM111112']
