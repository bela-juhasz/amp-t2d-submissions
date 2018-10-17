#!/bin/bash
#BSUB -J "Minimac[1-22]"
#BSUB -n 1 # request 8 cores
#BSUB -o "mimac3_%I.outI"
#BSUB -M 55000
#BSUB -e "mimac3_%I.err"
#BSUB -R "rusage[mem=50000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"

source ./1_Source.sh
mkdir -p minimac
#Minimac3 --refHaps $Ref/ALL.chr${LSB_JOBINDEX}.phase3_v5.shapeit2_mvncall_integrated.noSingleton.genotypes.vcf.gz --haps phased/phased.chr${LSB_JOBINDEX}.vcf.gz --rsid --prefix minimac/${LSB_JOBINDEX}.imputed --chr ${LSB_JOBINDEX} --doseOutput

Minimac3 --refHaps $Ref/ALL.chrX.Non.Pseudo.Auto.phase3_v5.shapeit2_mvncall_integrated.noSingleton.genotypes.vcf.gz --haps phased/24.Female.X.nonPAR.vcf.gz --rsid --prefix minimac/23.female.nonPAR.imputed --chr X --doseOutput

Minimac3 --refHaps $Ref/ALL.chrX.Non.Pseudo.Auto.phase3_v5.shapeit2_mvncall_integrated.noSingleton.genotypes.vcf.gz --haps phased/25.Male.X.nonPAR.vcf.gz --rsid --prefix minimac/23.male.nonPAR.imputed --chr X --doseOutput

Minimac3 --refHaps $Ref/ALL.chrX.Pseudo.Auto.phase3_v5.shapeit2_mvncall_integrated.noSingleton.genotypes.vcf.gz --haps phased/23.ALL.X.PAR.vcf.gz --rsid --prefix minimac/ALL.23.PAR.imputed --chr X --doseOutput

