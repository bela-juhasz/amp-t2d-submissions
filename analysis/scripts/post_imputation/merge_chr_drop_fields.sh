#!/bin/bash
#BSUB -J "secondpassfilt"
#BSUB -n 2 # request 8 cores
#BSUB -o "filt.o"
#BSUB -M 16000
#BSUB -e "filt.e"
#BSUB -R "rusage[mem=7000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"

#####
#
# Script set up for GoDarts imputed data
# concat chrs into one vcf index, drop fields again these may not be present we only want doasge in the output for bolt-Lmm
# Its very important to check with tabix that the files have been indexed correctly. $ tabix $file 22 | head
#
#####

bcftools concat --threads 8 -Oz -o GoDarts.affy.HRC.imputed.vcf.gz chr1.vcf.gz chr2.vcf.gz chr3.vcf.gz chr4.vcf.gz chr5.vcf.gz chr6.vcf.gz chr7.vcf.gz chr8.vcf.gz chr9.vcf.gz chr10.vcf.gz chr11.vcf.gz chr12.vcf.gz chr13.vcf.gz chr14.vcf.gz chr15.vcf.gz chr16.vcf.gz chr17.vcf.gz chr18.vcf.gz chr19.vcf.gz chr20.vcf.gz chr21.vcf.gz chr22.vcf.gz

tabix -p vcf GoDarts.affy.HRC.imputed.vcf.gz

bcftools annotate -x FORMAT/GT GoDarts.affy.HRC.imputed.vcf.gz | bcftools annotate -x FORMAT/GP -Oz -o Godarts.af.BOLT.vcf.gz

zcat Godarts.af.BOLT.vcf.gz | grep -v "#" | awk '{$6=$7=$8=$9=""; print $0}' | sed 's/ \+/ /g' | sed 's/ /\t/g' | perl -pe 's/^(\S+)\t(\S+)\t(\S+)\t(\S+)\t(\S+)/$3\t$1\t$2\t$5\t$4/;' | bgzip -c > Affy.BOLT.fin.ds.vcf.gz
