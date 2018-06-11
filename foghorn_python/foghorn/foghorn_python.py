import argparse

from vcf_comp_funcs import *

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
    outhandle = str(args.out) + "_GT.cvcf"
    out = open(outhandle, "w", 1)
    mis_vars = open("missing_vars_GT.txt", "w")
    compress_genotypes(sys.stdin, out, mis_vars)
    out.close()
    mis_vars.close()
elif args.dosage:
    outhandle = str(args.out) + "_DS.cvcf"
    out = open(outhandle, "w", 1)
    compress_dosages(sys.stdin, out)
    out.close()
