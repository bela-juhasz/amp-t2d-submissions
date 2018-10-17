#!/bin/sh
#BSUB -J "filter_merge"
#BSUB -n 1 # request 8 cores
#BSUB -o "11_filt.o"
#BSUB -M 35000
#BSUB -e "11_filt.e"
#BSUB -R "rusage[mem=35000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"
source 1_Source.sh

# filter R2

#bcftools.

#cftools filter --threads 12 -e 'MAF=0' Hoorn.HRC.imputed.vcf.gz -Oz -o Hoorn.filt.HRC.vcf.gz

for i in {1..22}; do bcftools filter -e 'MAF=0' chr${i}.dose.vcf.gz | bcftools filter -e 'R2<0.3' | bcftools filter -e 'AC<1' -Oz -o chr${i}.vcf.gz; done

bcftools filter -e 'MAF=0' chrX.merge.order.vcf.gz | bcftools filter -e 'R2<0.3' | bcftools filter -e 'AC<1' -Oz -o chr23.vcf.gz

bcftools concat --threads 8 -Oz -o Hoorn.HRC.imputed.vcf.gz chr1.vcf.gz chr2.vcf.gz chr3.vcf.gz chr4.vcf.gz chr5.vcf.gz chr6.vcf.gz chr7.vcf.gz chr8.vcf.gz chr9.vcf.gz chr10.vcf.gz chr11.vcf.gz chr12.vcf.gz chr13.vcf.gz chr14.vcf.gz chr15.vcf.gz chr16.vcf.gz chr17.vcf.gz chr18.vcf.gz chr19.vcf.gz chr20.vcf.gz chr21.vcf.gz chr22.vcf.gz chr23.vcf.gz
~   
