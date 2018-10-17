#!/bin/bash
#BSUB -J "firstpassfilt[1-22]"
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
# Needed to Zip with bgzip for tabix
# filter based on imputation quality and remove monomorphics
#
#####


zcat ../../Affy_HRCimputation2017/${LSB_JOBINDEX}.pbwt_reference_impute_clean_17082017.vcf.gz | bgzip -c > ../../Affy_HRCimputation2017/${LSB_JOBINDEX}.pbwt_reference_impute_clean_17082017_bgzip.vcf.gz; 

tabix -f -p vcf ../../Affy_HRCimputation2017/${LSB_JOBINDEX}.pbwt_reference_impute_clean_17082017_bgzip.vcf.gz; 

## This is dependent on whats in the VCF there may be R2 instead of INFO or no AC, MAF etc... however these can be annotated via bcftools 
bcftools filter -e 'MAF=0' ../../Affy_HRCimputation2017/${LSB_JOBINDEX}.pbwt_reference_impute_clean_17082017_bgzip.vcf.gz | bcftools filter -e 'INFO<0.4' | bcftools filter -e 'AC<1' -Oz -o chr${LSB_JOBINDEX}.vcf.gz;# done
