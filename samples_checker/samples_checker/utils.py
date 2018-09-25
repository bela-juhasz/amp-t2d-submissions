"""
Utility functions for samples checker
"""
# pylint: disable=no-member
import xml.etree.ElementTree as ET
import pysam

def get_samples_from_xml(sample_xml):
    """
    Get the {sample_id : genotype_id} hash from xml configuration file
    :param sample_xml: path to the xml configuration file
    :type sample_xml: basestring
    :return: mapping between sample_id and genotype_id
    :rtype: dict
    """
    sample_tree = ET.parse(sample_xml)
    sample_root = sample_tree.getroot()
    sample_ids = {sample.findtext('SAMPLE_ID') : sample.findtext('GENOTYPE_ID')
                  for sample in sample_root.findall('SAMPLE')}
    return sample_ids

def get_file_groups_from_xml(file_xml):
    """
    Get the file groups from xml configuration file in the form as
    {
        'file_type' : 'vcf',
        'file_names' : ['genotypes.4.vcf', 'genotypes.6.vcf']
    }
    :param file_xml: path to the xml configuration file
    :type file_xml: basestring
    :return: mapping for file_names and file_type
    :rtype: dict
    """
    file_tree = ET.parse(file_xml)
    file_root = file_tree.getroot()
    files = [ { 'file_type' : file_group.findtext('FILE_TYPE'),
                'file_names' : [ file_name.text for file_name in file_group.findall('FILE')] }
             for file_group in file_root.findall('FILE_GROUP') ]
    return files

def get_samples_from_file_group(file_group, file_path):
    """
    Get the set of the samples appear in the file group.
    :param file_group: mapping for file_names and file_type
    :type file_group: dict
    :param file_path: the path to the directory where files could be found
    :type file_path: basestring
    :return: Sample set
    :rtype: set
    """
    samples = set([])
    file_type = file_group.get('file_type', '')
    if file_type and file_type in FILE_TYPE_TO_FUNCTION:
        file_names = file_group.get('file_names', [])
        for file_name in file_names:
            samples = samples.union(set(FILE_TYPE_TO_FUNCTION[file_type](file_path + '/' + file_name)))
    return samples


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

def get_sample_difference(submission_samples, samples_from_submitted_files, submitted_file_type):
    """
    Get the set difference between the submission_samples and the samples found in submitted_file
    :param submission_samples: mapping between sample_id and genotype_id from submission xls
    :type submission_samples: dict
    :param samples_from_submitted_files: samples from the submitted files
    :type samples_from_submitted_files: set
    :param submitted_file_type: the type of the submitted file, e.g.: vcf
    :type submitted_file_type: basestring
    :return: two lists of submission_samples
    :rtype: multiple lists
    """

    # Check arguments
    if not submission_samples or not submitted_file_type or not samples_from_submitted_files:
        return [], []

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
                                          set(samples_from_submitted_files))
    diff_submitted_file_submission = list(set(samples_from_submitted_files)-
                                          set(samples_from_submission))

    return diff_submission_submitted_file, diff_submitted_file_submission

FILE_TYPE_TO_FUNCTION = {
    'vcf':  get_samples_from_vcf
}
