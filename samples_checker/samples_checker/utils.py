"""
Utility functions for samples checker
"""
# pylint: disable=no-member
from lxml import etree
import pysam

def get_samples_from_xml(sample_xml):
    """
    Get the {sample_id : genotype_id} hash from xml configuration file
    :param sample_xml: path to the xml configuration file
    :type sample_xml: basestring
    :return: mapping between sample_id and genotype_id
    :rtype: dict
    """
    sample_tree = etree.parse(sample_xml)
    sample_root = sample_tree.getroot()
    sample_ids = {sample.findtext('SAMPLE_ID') : sample.findtext('GENOTYPE_ID')
                  for sample in sample_root.findall('SAMPLE')}
    return sample_ids

def get_files_from_xml(file_xml):
    """
    Get the {file_name : file_type} has from xml configuration file
    :param file_xml: path to the xml configuration file
    :type file_xml: basestring
    :return: mapping between file_name and file_type
    :rtype: dict
    """
    file_tree = etree.parse(file_xml)
    file_root = file_tree.getroot()
    files = {file.findtext('FILE_NAME') : file.findtext('FILE_TYPE')
             for file in file_root.findall('FILE')}
    return files

def get_samples_from_vcf(vcf_file):
    """
    Get the list of samples from the VCF file
    :param vcf_file: path to the VCF file
    :type vcf_file: basestring
    :return: list of sample names
    :rtype: list
    """
    vcf_in = pysam.VariantFile(vcf_file, 'r')
    vcf_header = vcf_in.header
    samples = list(vcf_header.samples)
    vcf_in.close()
    return samples

def get_sample_ids(samples):
    """
    Get the list of sample ids from the {sample_id : genotype_id} hash
    :param samples: mapping between sample_id and genotype_id
    :type samples: dict
    :return: list of sample names
    :rtype: list
    """
    return samples.keys()

def get_genotype_ids(samples):
    """
    Get the list of genotype ids from the {sample_id : genotype_id} hash
    If the genotype_id is empty then use the sample_id by default
    :param samples: mapping between sample_id and genotype_id
    :type samples: dict
    :return: list of genotype ids
    :rtype: list
    """
    return [samples[key] if samples[key] else key for key in samples]

def check_samples_in_file(samples, file_name, file_type):
    """
    Check that all the samples contained in the file_name are found in the samples
    :param samples: mapping between sample_id and genotype_id
    :type samples: dict
    :param file_name: path to the file
    :type file_name: basestring
    :param file_type: the type of the file, e.g.: vcf
    :type file_type: basestring
    :return: list of samples that are not found
    :rtype: list
    """
    if not samples or not file_type or not file_name:
        return []

    if file_type not in FILE_TYPE_TO_FUNCTION:
        return []

    samples_in_file = FILE_TYPE_TO_FUNCTION[file_type](file_name)

    sample_ids = []
    if file_type == 'vcf':
        sample_ids = get_genotype_ids(samples)
    else:
        sample_ids = get_sample_ids(samples)

    return list(set(samples_in_file)-set(sample_ids))

FILE_TYPE_TO_FUNCTION = {
    'vcf':  get_samples_from_vcf
}
