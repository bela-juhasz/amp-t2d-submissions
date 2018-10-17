#!/bin/bash
#BSUB -J 8_OUT
#BSUB -n 4 # request 8 cores
#BSUB -o "bsub_logs/8_OUT.out"
#BSUB -M 16000
#BSUB -e "bsub_logs/8_OUT.err"
#BSUB -R "rusage[mem=16000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"

source ./1_Source.sh 

shapeit -B $DATA/Chr23.align --chrX --force -T 8 -M $Ref/genetic_map_chr23_combined_b37.txt -O phased/phased.chr23 --output-log logs/chr23phased.log

shapeit -convert \
        --input-haps phased/phased.chr23 \
        --output-vcf phased/phased.chr23.vcf;
bgzip phased/phased.chr23.vcf
tabix -p vcf phased/phased.chr23.vcf

awk '$6==2 {print $2}' phased/phased.chr22.sample > phased/Female.samples
awk '$6==1 {print $2}' phased/phased.chr22.sample > phased/Male.samples

bcftools view --force-samples -S phased/Male.samples phased/phased.chr23.vcf.gz | bgzip -c > phased/Male.23.vcf.gz
bcftools view --force-samples -S phased/Female.samples phased/phased.chr23.vcf.gz | bgzip -c > phased/Female.23.vcf.gz

tabix -p vcf phased/Male.23.vcf.gz
tabix -p vcf phased/Female.23.vcf.gz


#######
#
# NON-PAR-PAR can be split here
# HG19 2699520 & 154931044 are boundaries 
#
#######

bcftools view -r 23:1-2699520 phased/phased.chr23.vcf.gz -Oz -o phased/PAR1.ALL.vcf.gz
bcftools view -r 23:154931044-1549310440 phased/phased.chr23.vcf.gz -Oz -o phased/PAR2.ALL.vcf.gz # tacked a zeor on the end to exceed chr length
bcftools view -r 23:2699520-154931044 phased/Male.23.vcf.gz -Oz -o phased/nonPAR.Male.vcf.gz
bcftools view -r 23:2699520-154931044 phased/Female.23.vcf.gz -Oz -o phased/nonPAR.Female.vcf.gz
bcftools concat phased/PAR1.ALL.vcf.gz phased/PAR2.ALL.vcf.gz | bcftools sort -Oz -o phased/ALL.23.PAR.vcf.gz

tabix -p vcf phased/ALL.23.PAR.vcf.gz
tabix -p vcf phased/nonPAR.Male.vcf.gz
tabix -p vcf phased/nonPAR.Female.vcf.gz

#minimac want 23 as X
bcftools annotate --rename-chrs phased/rename_X phased/ALL.23.PAR.vcf.gz -Oz -o phased/23.ALL.X.PAR.vcf.gz
bcftools annotate --rename-chrs phased/rename_X phased/nonPAR.Female.vcf.gz -Oz -o phased/24.Female.X.nonPAR.vcf.gz
bcftools annotate --rename-chrs phased/rename_X phased/nonPAR.Male.vcf.gz -Oz -o phased/25.Male.X.nonPAR.vcf.gz


for i in {1..25}; do
       shapeit -B $DATA/Chr${i}.align -T 8 -M $Ref/genetic_map_chr${i}_combined_b37.txt -O phased/phased.chr${i} --output-log logs/chr${i}phased.log;
done

for j in {1..25}; do
shapeit -convert \
        --input-haps phased/phased.chr${j} \
        --output-vcf phased/phased.chr${j}.vcf;
bgzip phased/phased.chr${j}.vcf;
tabix -p vcf phased/phased.chr${j}.vcf.gz
done

