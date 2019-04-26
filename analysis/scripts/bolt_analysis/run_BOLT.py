from __future__ import print_function
from __future__ import division
import sys
import os
from subprocess import call
traits = ["GLU_FAST","HBA1C_PCT","HBA1C_MMOL","GAD_AB","SERUM_CREATININE","CHOL","LDL_CALCULATED","HDL","TG","EGFR","ACR","HEIGHT_CM","WEIGHT_KG","SBP","DBP","CREAT_URINARY","ALB_URINARY","ACR_URINARY","BMI","eGFR1","GLU_FAST_ADJ","HBA1C_PCT_ADJ","HBA1C_MMOL_ADJ","SERUM_CREATININE_ADJ","CHOL_ADJ","LDL_CALCULATED_ADJ","HDL_ADJ","TG_ADJ","EGFR_ADJ","ACR_ADJ","HEIGHT_CM_ADJ","WEIGHT_KG_ADJ","SBP_ADJ","DBP_ADJ","CREAT_URINARY_ADJ","ALB_URINARY_ADJ","ACR_URINARY_ADJ","BMI_ADJ","eGFR1_ADJ"]
bsub_prefix = "bsub -R 'select[mem>5000] rusage[mem=5000]' -M5000 -q analysis-rh7 "
for trait in traits:
    if(trait=="ACR_URINARY_ADJ"):
        continue
    e_o = "-e "+trait+".e -o "+trait+".o "
    cmd = "bolt --bfile Hoorn_v2_BOLT_GRM_SNPS --phenoFile=final_modified_v2.phenotype --phenoCol "+trait+" --geneticMapFile /homes/dbennett/bin/BOLT-LMM_v2.3.2/tables/genetic_map_hg19_withX.txt.gz --LDscoresFile /homes/dbennett/bin/BOLT-LMM_v2.3.2/tables/LDSCORE.1000G_EUR.tab.gz --numThreads 20 --lmm --statsFile results/Hoorn_v2."+trait+".GRM --maxMissingPerSnp 0.05 --qCovarCol PC{1:10} --covarFile PCA_hrd_call.eigenvec --maxModelSnps 1400000 --LDscoresMatchBp --dosageFile Hoorn_v2.BOLT.fin_ds.vcf.gz --lmmForceNonInf --statsFileDosageSnps results/Hoorn_v2."+trait+".dosage.gz --dosageFidIidFile BOLT_v2.indivs.txt"
    full_cmd = bsub_prefix+e_o+"\""+cmd+"\""
    #print(full_cmd)
    call(full_cmd,shell=True)