#!/bin/bash
#Parses a PLINK bim file and captures any palindromic SNPs
awk 'BEGIN{FS="\t"; OFS="\t";} {if (($5 == "A" && $6 == "T") || ($5 == "T" && $6 == "A") || ($5 == "C" && $6 == "G") || ($5 == "G" && $6 == "C")) print $0}'
