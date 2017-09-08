#!/bin/bash
#Subscript for finding the raw frequencies of the data
WORKSPACE=$1
SCRIPT_DIR=$2
INPUT_STEM=$3

mkdir -p $WORKSPACE
pushd $WORKSPACE

plink --bfile $INPUT_STEM --freq --out raw

#Create clean copies of the reports
cat raw.frq | sh $SCRIPT_DIR/clean_plink_report.sh > clean.frq

#Create concise copies of the report
cat clean.frq | cut -f 2,5 | sed 1d | sort -k 1,1 > concise.frq

#Now create buckets for various MAF thresholds
cat concise.frq | awk 'BEGIN{FS="\t"; OFS="\t"} {if ($2 < 0.01) print $1}' > lt_1pc_maf.markers
cat concise.frq | awk 'BEGIN{FS="\t"; OFS="\t"} {if ($2 >= 0.01) print $1}' > gte_1pc_maf.markers

popd
