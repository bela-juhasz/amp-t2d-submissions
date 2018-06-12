"""
This script compresses genotypes or dosages information stored in a VCF file.
"""
from __future__ import print_function
import argparse
from foghorn_compression import *

param = sys.argv

parser = argparse.ArgumentParser(prog="unzip_test_tool.py", formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="Command line python tool for transforming VCF files into cVCF files as required by the AMP-T2D GAIT analysis machines" + "\n" + "GT flag will compress genotypes splitting multialleic sites on to two lines." + "\n" + "The DS flag will compress dosage format. Currently not implemented for multi-allelics" + "\n" + "\n" + "Usage:" + "\n" + "zcat inVCF.vcf.gz | python tool.py -o outfile -GT[DS]")
parser.add_argument("-i", "--vcf", help="Vcf file required. please pipe from zcat", type=argparse.FileType('r'),
                    default=sys.stdin)
parser.add_argument("-o", "--out", help="Name of outfile", default="out")
parser.add_argument("-GT", "--genotype", help="Select for genotype transformation", action="store_true")
parser.add_argument("-DS", "--dosage", help="Select for dosage transformation", action="store_true")
args = parser.parse_args()

if args.genotype:
    out_filename = str(args.out) + "_genotypes.cvcf"
    try:
        output = open(out_filename, "w", 1)
        missing_vars = open("missing_vars_genotypes.txt", "w")
        compress_genotypes(sys.stdin, output, missing_vars)
        output.close()
        missing_vars.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror), file=sys.stderr)
        quit(1)
elif args.dosage:
    out_filename = str(args.out) + "_dosages.cvcf"
    try:
        output = open(out_filename, "w", 1)
        compress_dosages(sys.stdin, output)
        output.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror), file=sys.stderr)
        quit(1)
else:
    print('Please select either genotype or dosage for processing.', file=sys.stderr)
    quit(1)
