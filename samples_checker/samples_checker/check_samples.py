"""
This script checks if a submission xls contains all samples that exist in the submitted files
"""
# pylint: disable=C0103
from __future__ import print_function
import sys
import argparse
import utils

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

submission_samples = utils.get_samples_from_xml(sample_xml)
submitted_files = utils.get_files_from_xml(file_xml)

has_difference = False
for file_name in submitted_files:
    file_type = submitted_files.get(file_name, '')
    difference_submission_xls_submitted_file, difference_submitted_file_submission_xls =\
        utils.get_sample_difference(submission_samples, file_path + '/' + file_name, file_type)

    if difference_submitted_file_submission_xls:
        has_difference = True
        if file_type == 'vcf':
            print('The submission does not contain the following genotype ids:', file=sys.stderr)
        else:
            print('The submission does not contain the following samples:', file=sys.stderr)
        print(difference_submitted_file_submission_xls, file=sys.stderr)

    if difference_submission_xls_submitted_file:
        has_difference = True
        print('The following samples are not found in file '+file_name, file=sys.stderr)
        print(difference_submission_xls_submitted_file, file=sys.stderr)

if has_difference:
    quit(1)

print('Samples checking completed!', file=sys.stdout)
