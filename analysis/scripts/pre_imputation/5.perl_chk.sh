#!/bin/bash
#BSUB -J 5_OUT
#BSUB -o "bsub_logs/5_OUT.out"
#BSUB -n 1
#BSUB -e "bsub_logs/5_OUT.err"
#BSUB -M 60000
#BSUB -R 'rusage[mem=25000]'
#BSUB -R 'span[hosts=1]'
#BSUB -q "analysis-rh7"


COLUMNS=80 ; export COLUMNS
LINES=21; export LINES

source ./1_Source.sh

perl HRC-1000G-check-bim.pl -b t2d_snp_qc.bim -f t2d_snp_qc.frq -r $REFlegend -g -p $POP

