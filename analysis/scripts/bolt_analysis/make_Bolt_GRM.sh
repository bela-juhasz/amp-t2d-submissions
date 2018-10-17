#!/bin/bash
#BSUB -J "mk_GRM" # make this the length of the variable traits
#BSUB -n 1 # request 8 cores
#BSUB -o "GRM.out"
#BSUB -M 5000
#BSUB -e "GRM.err"
#BSUB -R "rusage[mem=5000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "development-rh7"

# makes a subset of the hard-called data and LD prunes

plink --bfile ../../Illumina_HRCimputation2017/AMPLOAD7.illumina.hrd --indep-pairwise 50 5 0.2 --out prune

plink --bfile ../../Illumina_HRCimputation2017/AMPLOAD7.illumina.hrd --extract prune.prune.in --hwe 0.000005 --geno 0.02 --maf 0.01 --make-bed --out Bolt.illumina.GRM
