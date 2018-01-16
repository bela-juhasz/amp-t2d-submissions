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

def get_sample_difference(submission_samples, submitted_file, submitted_file_type):
    """
    Get the set difference between the submission_samples and the samples found in submitted_file
    :param submission_samples: mapping between sample_id and genotype_id from submission xls
    :type submission_samples: dict
    :param submitted_file: path to the submitted file
    :type submitted_file: basestring
    :param submitted_file_type: the type of the submitted file, e.g.: vcf
    :type submitted_file_type: basestring
    :return: two lists of submission_samples
    :rtype: multiple lists
    """

    # Check arguments
    if not submission_samples or not submitted_file_type or not submitted_file:
        return [], []

    # Make sure we know how to get the samples out of submitted_file
    if submitted_file_type not in FILE_TYPE_TO_FUNCTION:
        return [], []

    # Get the sample set out of submitted_file
    samples_from_submitted_file = FILE_TYPE_TO_FUNCTION[submitted_file_type](submitted_file)

    # Get the sample set from submission template
    samples_from_submission = []
    if submitted_file_type == 'vcf':
        # this is a special case for AMP where you can specify a geno id for a sample.
        # the geno id is used in the vcf file.
        # for other submitted vcf file, you will still get the samples keys.
        samples_from_submission = get_genotype_ids(submission_samples)
    else:
        # for everything else, just get the keys from submission_samples dictionary
        samples_from_submission = get_sample_ids(submission_samples)

    # Get the bi-directional set differences between above two sets.
    diff_submission_submitted_file = list(set(samples_from_submission)-
                                          set(samples_from_submitted_file))
    diff_submitted_file_submission = list(set(samples_from_submitted_file)-
                                          set(samples_from_submission))

    return diff_submission_submitted_file, diff_submitted_file_submission

FILE_TYPE_TO_FUNCTION = {
    'vcf':  get_samples_from_vcf
}
