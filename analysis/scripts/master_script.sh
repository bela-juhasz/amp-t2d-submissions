#Generation of plink files from normallized VCF
plink --make-bed --out Hoorn_plink_files --vcf Hoorn_v2_normalized.vcf.gz
#Pipeline for pre-imputation. Modify 1_Source.sh accordingly and run 1b_update_build.sh if needed.
bash 2.Sample_QC.sh
bash 3.Sample_QC.sh
bash 4.SNP_QC.sh
bash 5.perl_chk.sh
bash 6.tidy_perl.sh
bash 7.disconcordance_chk.sh
#Imputation on Michigan server needs to be performed manually. Output files then need to be copied into directory and unzipped.
#Post-imputation merge and filter of vcf
python zip_tabix_filter.py
python zip_tabix_filter_chrX.py
bcftools concat --threads 8 -Oz -o Hoorn_v2_joint_imputed.vcf.gz chr1.vcf.gz chr2.vcf.gz chr3.vcf.gz chr4.vcf.gz chr5.vcf.gz chr6.vcf.gz chr7.vcf.gz chr8.vcf.gz chr9.vcf.gz chr10.vcf.gz chr11.vcf.gz chr12.vcf.gz chr13.vcf.gz chr14.vcf.gz chr15.vcf.gz chr16.vcf.gz chr17.vcf.gz chr18.vcf.gz chr19.vcf.gz chr20.vcf.gz chr21.vcf.gz chr22.vcf.gz chr23.vcf.gz
#bcftools filter --threads 12 -e MAF=0 -Oz -o Hoorn_v2_filt.vcf.gz Hoorn_v2_joint_imputed.vcf.gz - This is already done in zip_tabix_filter.py
bcftools annotate -x FORMAT/GP -Oz -o Hoorn_v2.GP.dropped.vcf.gz Hoorn_v2_joint_imputed.vcf.gz
bcftools plugin fill-tags -Oz -o Hoorn_v2.AC.vcf.gz -- Hoorn_v2.GP.dropped.vcf.gz -t AF,AC,AN
#Foghorn Transform
zcat Hoorn_v2.GP.dropped.vcf.gz | python foghorn_main.py -o Hoorn_V2 -GT
zcat Hoorn_v2.GP.dropped.vcf.gz | python foghorn_main.py -o Hoorn_V2_dosage -DS
bgzip  Hoorn_V2_genotypes.cvcf
tabix -s 1 -b 2 -e 2 -c "#” Hoorn_V2_genotypes.cvcf.gz
bgzip Hoorn_V2_dosage_dosages.cvcf
tabix -s 1 -b 2 -e 2 -c “#” Hoorn_V2_dosage_dosages.cvcf.gz
#PCA for eigen vector and value estimation
plink --out PCA.Hoorn_v2 --pca 10 header --vcf Hoorn_v2.GP.dropped.vcf.gz
#BOLT analysis
bash get_info_bins_modified.sh
plink --make-bed --out Hoorn_v2_info1 --vcf Hoorn_v2_INFO_1.vcf.gz
plink --bfile Hoorn_v2_info1 --indep-pairwise 500 50 0.8 --out thinned
plink --bfile Hoorn_v2_info1 --out PCA_hrd_call --pca header
plink --bfile Hoorn_v2_info1 --extract thinned.prune.in --make-bed --out Hoorn_v2_BOLT_GRM_SNPS
bcftools_annotateCommand=annotate -x FORMAT/GT -Oz -o Hoorn_v2.BOLT.vcf.gz Hoorn_v2.GP.dropped.vcf.gz
python fin_ds_generation.py
python modify_sample_list.py
python run_BOLT.py
#Phenotype normalization
python add_additional_pheno_columns.py
python add_sex_to_pheno_original.py
#Run commands from  modified_R_commands.txt on R to generate normalized/adjusted values for phenotypes and their corresponding plots
python remove_filtered_samples_from_sample_file.py
#Push to KP