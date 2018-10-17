#!/bin/bash
#BSUB -J 4_OUT
#BSUB -n 2 # request 8 cores
#BSUB -o "bsub_logs/4_OUT.out"
#BSUB -M 16000
#BSUB -e "bsub_logs/4_OUT.err"
#BSUB -R "rusage[mem=16000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"


source ./1_Source.sh

plink --bfile T2D --geno $GENO --maf $MAF --freq --make-bed --out t2d_snp_qc

# tidy
mv *iss *het *check *genome QC/
mv *log logs

rm temp_t2d_3* temp_t2d.* prune* exclud* t2d.* t2d_rem*

rm temp*
rm prune*

