#!/bin/sh
#BSUB -J "IMPUTATION_PIC"
#BSUB -n 1 # request 8 cores
#BSUB -o "PIC.o"
#BSUB -M 35000
#BSUB -e "PIC.e"
#BSUB -R "rusage[mem=35000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"
source 1_Source.sh

for i in {1..23}; do tabix -p vcf minimac/${i}.imputed.dose.vcf.gz; done


#### merge X chromosome 
#23.female.nonPAR.imputed.dose.vcf.gz
#ALL.23.PAR.imputed.dose.vcf.gz
#23.male.nonPAR.imputed.dose.vcf.gz

bcftools merge minimac/23.female.nonPAR.imputed.dose.vcf.gz minimac/23.male.nonPAR.imputed.dose.vcf.gz -Oz -o minimac/ALL.23.nonPAR.imputed.dose.vcf.gz
tabix -p vcf minimac/ALL.23.nonPAR.imputed.dose.vcf.gz
tabix -H minimac/ALL.23.nonPAR.imputed.dose.vcf.gz | tr "\t" "\n" | grep -v "##" | tail -n +10 > minimac/nonPAR.header
bcftools view --force-samples -S minimac/non_PAR.header minimac/ALL.23.PAR.imputed.dose.vcf.gz | bgzip -c > minimac/PAR.reordered.vcf.gz
tabix -p vcf minimac/nonPAR.reordered.vcf.gz 
bcftools merge minimac/ALL.23.nonPAR.imputed.dose.vcf.gz minimac/PAR.reordered.vcf.gz -Oz -o minimac/23.imputed.dose.vcf.gz

mkdir -p minimac/imp_vcf

for i in {1..23}; do mv minimac/${i}.imputed.dose.vcf.gz minimac/imp_vcf; done


#### mv to VCF directory minimac/imp_vcf


# Post imputation checking

perl /homes/dbennett/bin/IC/vcfparse.pl -d ./minimac/imp_vcf -g -o vcfparse
#perl /homes/dbennett/bin/IC/ic.pl -d ./vcfparse -r ~/HRC.r1-1.GRCh37.wgs.mac5.sites.tab -h -o POSTIC #hrc
perl /homes/dbennett/bin/IC/ic.p -d ./vcfparse -r $Ref/1000GP_Phase3_combined.legend -g -p EUR -o POSTIC #G1K

