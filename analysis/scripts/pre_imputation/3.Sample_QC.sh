#!/bin/bash
#BSUB -J 3_OUT
#BSUB -n 4 # request 8 cores
#BSUB -o "bsub_logs/3_OUT.out"
#BSUB -M 16000
#BSUB -e "bsub_logs/3_OUT.err"
#BSUB -R "rusage[mem=16000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"

source ./1_Source.sh

# Remove ambiguous Sex Calls
grep PROBLEM t2d.sexcheck | awk '{print $1,$2}' > remove.indiv.txt

# R script to Remove heterozygots that fall outside med + (3*IQR)
Rscript het.r t2d.het # produces 2 files a pass and fail file
# Print indivs to file 
awk '{print $2,$3}' Heterozygosity_remove.out > remove_Hets.txt

# Cryptic relatedness hash the indiv pairs and filter on missingness. 
#python genome_missing_remove.py temp_t2d_3.genome temp_t2d_3.imiss 0.185

# concat fail indivs 
cat remove* > rem.ind.txt

# nonmissing nonmale Y chromosomes
#cat *hh | sort -k1 | uniq >> rem.ind.txt
sort -u rem.ind.txt > rem1_file.txt

rm rem.ind.txt

sed -i 's/\t/ /g' rem1_file.txt
awk '{print $1,$2}' rem1_file.txt | sort -u > rem_file.txt
rm rem1_file.txt

# remove individuals
plink --bfile t2d --remove rem_file.txt --make-bed --out t2d_rem

awk '{print $3}' t2d_rem.hh | sort -u > rem_snp.txt
plink --bfile t2d_rem --exclude rem_snp.txt --make-bed --out T2D


