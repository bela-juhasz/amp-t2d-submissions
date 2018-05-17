#!/usr/bin/python2.7
from SumStat_funs import * 
import sys, argparse

parser = argparse.ArgumentParser(prog="SumstatUpdate.py", formatter_class=argparse.RawDescriptionHelpFormatter,description="Command line python tool for validating and aligning Summary Statistics"+"\n" +"\n"+"Summary statistics for mis-aligned variants will be updated as well as monomorphic associations removed"+"\n"+"\n"+"When -B chosen Beta values will be converted to Odds Ratios"+"\n"+"\n" + "Minor allele count,freq and effect allele freq are also calculated")
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-S","--SummaryStat", help="Genetic association file required")
requiredNamed.add_argument("-R","--Reference", help="Reference genome fasta file")
parser.add_argument("-B","--Binary",help="Select for binary traits", action="store_true")
args = parser.parse_args()

if not args.Binary:
	print Rvtests_Quan(args.SummaryStat, args.Reference)
	print "Quantitative selected"
else:
	print Rvtests_bin(args.SummaryStat, args.Reference)
	print "Binary selected"
