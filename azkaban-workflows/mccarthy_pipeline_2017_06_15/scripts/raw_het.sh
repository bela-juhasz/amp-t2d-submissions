#!/bin/bash
#Subscript for finding the raw heterozygosity of the data

WORKSPACE=$1
SCRIPT_DIR=$2
INPUT_STEM=$3
RAW_FREQ_DIR=$4

mkdir -p $WORKSPACE
pushd $WORKSPACE

#Run the HET at different MAF cutoffs
plink --bfile $INPUT_STEM --het --out all
plink --bfile $INPUT_STEM --extract $RAW_FREQ_DIR/lt_1pc_maf.markers --het --out lt_1pc
plink --bfile $INPUT_STEM --extract $RAW_FREQ_DIR/gte_1pc_maf.markers --het --out gte_1pc

#Create clean copies of the reports
cat all.het | sh $SCRIPT_DIR/clean_plink_report.sh | cut -f 1,2,3,5 | sed 1d > clean.all.het
cat lt_1pc.het | sh $SCRIPT_DIR/clean_plink_report.sh | cut -f 1,2,3,5 | sed 1d > clean.lt_1pc_maf.het
cat gte_1pc.het | sh $SCRIPT_DIR/clean_plink_report.sh | cut -f 1,2,3,5 | sed 1d > clean.gte_1pc_maf.het

popd
