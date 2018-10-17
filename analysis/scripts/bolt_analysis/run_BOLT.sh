#!/bin/bash
#BSUB -J "arrayBOLT-LMM_adj[1-53]" # make this the length of the variable traits
#BSUB -n 1 # request 8 cores
#BSUB -o "aBOLT.out%I"
#BSUB -M 5000
#BSUB -e "aBOLT.err%I"
#BSUB -R "rusage[mem=5000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"
#CHR=$1
####
# Make bolt dosage format. first drop everything except doasge in vcf
# then 
# zcat Hoorn.BOLT.vcf.gz | grep -v "#" | awk '{$6=$7=$8=$9=""; print $0}' | sed 's/ \+/ /g' | sed 's/ /\t/g' | perl -pe 's/^(\S+)\t(\S+)\t(\S+)\t(\S+)\t(\S+)/$3\t$1\t$2\t$5\t$4/;' | bgzip -c > Hoorn.BOLT.fin.ds.vcf.gz

# make Bolt.indivs 

tabix -H 5.pbwt_reference_impute_clean_17082017_bgzip.vcf.gz | tr "\t" "\n" | grep -v "#" | tail -n +9 | awk '{print $1,$1}' > Bolt.indivs


declare -a traits=(BURN_Var eGFR_ADJ eGFR GLU_FAST HBA1C_PCT HBA1C_11OL GAD_AB SERUM_CREATININE CHOL LDL_CALCULATED HDL TG LIPID_MED_LIPIDS STATIN_LIPIDS HEIGHT_CM WEIGHT_KG DBP HYPERTENSION HTN_MED_BP CREAT_URINARY ALB_URINARY ACR_URINARY CURRENT_SMOKE HDL_adj LDL_adj ACR_URINARY_adj CHOL_adj HBA1C_MMOL_adj ALB_URINARY_adj CREAT_URINARY_adj HBA1C_PCT_adj SERUM_CREAT_adj BMI_adj GLU_FAST_adj LOG_TG_adj HYPERTENSION_unadj STATIN_LIPIDS_unadj WEIGHT_ADJ HEIGHT_ADJ DBP_unadj BMI BMI_ADJ)

#declare -a traits=(BURN_VAR SBP_ADJ DBP_ADJ)


pheno=${traits[$LSB_JOBINDEX]} 
bolt --bfile BOLT_GRM_SNPS \ 
    --phenoFile=final_Hoorn.phenotype \
    --phenoCol $pheno \
    --geneticMapFile /homes/dbennett/bin/BOLT-LMM_v2.3.2/tables/genetic_map_hg19_withX.txt.gz \
    --LDscoresFile /homes/dbennett/bin/BOLT-LMM_v2.3.2/tables/LDSCORE.1000G_EUR.tab.gz \
    --numThreads 20 \
    --lmm \
    --statsFile results/Hoorn.$pheno.GRM \
    --maxMissingPerSnp 0.05 \
    --qCovarCol PC{1:10} \
    --covarFile PCA_hrd_call.eigenvec \
    --maxModelSnps 1400000 \
    --LDscoresMatchBp \
    --dosageFile Hoorn.BOLT.fin.ds.vcf.gz \
    --lmmForceNonInf \
    --statsFileDosageSnps results/Hoorn.$pheno.dosage.gz \
    --dosageFidIidFile Bolt.indivs;
 

