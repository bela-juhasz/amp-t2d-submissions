"""
This script checks if a submission xls contains all samples that exist in the submitted files
"""
# pylint: disable=C0103
from __future__ import print_function
import sys
import argparse
import utils


def get_sample_diff(file_path, file_xml, sample_xml):
    """
    Check the difference between samples specified in sample_xml and ones contained in the files
    Output any difference found and exit the program with code 1 if there is difference.
    specified in the file_xml.
    :param file_path: directory where the files specified in the file_xml could be found
    :type file_path: basestring
    :param file_xml: path to the xml file which contains the file groups information for retrieving samples
    :type file_xml: basestring
    :param sample_xml: path to the xml file which contains the sample elements.
    :type sample_xml: basestring
    """
    submission_samples = utils.get_samples_from_xml(sample_xml)
    submitted_file_groups = utils.get_file_groups_from_xml(file_xml)
    has_difference = False
    for submitted_file_group in submitted_file_groups:
        file_type = submitted_file_group.get('file_type', '')
        samples_from_submitted_files = utils.get_samples_from_file_group(submitted_file_group, file_path)
        difference_submission_xls_submitted_file, difference_submitted_file_submission_xls = \
            utils.get_sample_difference(submission_samples, samples_from_submitted_files, file_type)

        if difference_submitted_file_submission_xls:
            has_difference = True
            if file_type == 'vcf':
                print('Samples that appear in the VCF but not in the Metadata sheet:', file=sys.stderr)
            else:
                print('The submission does not contain the following samples:', file=sys.stderr)
            print(difference_submitted_file_submission_xls, file=sys.stderr)

        if difference_submission_xls_submitted_file:
            has_difference = True
            print('Samples that appear in the Metadata sheet but not in the submitted file(s):',
                  file=sys.stderr)
            print(difference_submission_xls_submitted_file, file=sys.stderr)
    if not has_difference:
        print('No differences found between the samples in the Metadata sheet and the submitted file(s)!',
              file=sys.stdout)
    print('Samples checking completed!', file=sys.stdout)
    if has_difference:
        quit(1)


def main():
    arg_parser = argparse.ArgumentParser(description='Check submission xls contains all samples that'
                                                     'exist in the submitted files')
    arg_parser.add_argument('--sample-xml', required=True, dest='samplexml',
                            help='XML file containing submission samples')
    arg_parser.add_argument('--file-xml', required=True, dest='filexml',
                            help='XML file containing submitted files')
    arg_parser.add_argument('--file-path', required=True, dest='filepath',
                            help='Path to the directory in which submitted files can be found')

    args = arg_parser.parse_args()
    sample_xml = args.samplexml
    file_xml = args.filexml
    file_path = args.filepath

    get_sample_diff(file_path, file_xml, sample_xml)


if __name__ == "__main__":
    main()
