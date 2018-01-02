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
                        help='XML file containing samples')
arg_parser.add_argument('--file-xml', required=True, dest='filexml',
                        help='XML file containing files')
arg_parser.add_argument('--file-path', required=True, dest='filepath',
                        help='Path to the directory in which submitted files can be found')

args = arg_parser.parse_args()
sample_xml = args.samplexml
file_xml = args.filexml
file_path = args.filepath

samples = utils.get_samples_from_xml(sample_xml)
files = utils.get_files_from_xml(file_xml)

has_difference = False
for file_name in files:
    difference = utils.check_samples_in_file(samples, file_path+'/'+file_name,
                                             files.get(file_name, ''))

    if difference:
        has_difference = True
        print('The submission does not contain the following samples in file '+file_name,
              file=sys.stderr)
        print(list(difference), file=sys.stderr)

if has_difference:
    quit(1)

print('Samples checking completed!', file=sys.stdout)
