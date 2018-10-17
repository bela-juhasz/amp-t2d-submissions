#!/bin/bash
#BSUB -J 6_OUT
#BSUB -n 4 # request 8 cores
#BSUB -o "bsub_logs/6_OUT.out"
#BSUB -M 16000
#BSUB -e "bsub_logs/6_OUT.err"
#BSUB -R "rusage[mem=16000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"

source ./1_Source.sh

chmod 755 Run-plink.sh
./Run-plink.sh


# above command will need to be changed to make output vcf dont need to split chromosomes
echo -e $'\n \n writing VCF into GWAS_data \n \n'

for h in {1..23}; do
       plink --bfile t2d_snp_qc-updated-chr${h} --make-bed --out GWAS_data/myGwasData.chr${h};
done

rm t2d_snp_qc-updated*

mv Chromosome-t2d_snp_qc-1000G.txt Exclude-t2d_snp_qc-1000G.txt Force-Allele1-t2d_snp_qc-1000G.txt FreqPlot-t2d_snp_qc-1000G.txt ID-t2d_snp_qc-1000G.txt LOG-t2d_snp_qc-1000G.txt Position-t2d_snp_qc-1000G.txt Strand-Flip-t2d_snp_qc-1000G.txt strand_checkerout/
