#!/bin/bash
#Subscript for excluding the roughest indivs and markers from the lab

WORKSPACE=$1
INPUT_STEM=$2
RAW_MISSING_DIR=$3

mkdir -p $WORKSPACE
pushd $WORKSPACE

#Go to the RAW_MISSING directory and grap the exclusion set from the cleaned i/lmiss files

#Throw out any indiv > 5% missing
cat $RAW_MISSING_DIR/clean.imiss | awk 'BEGIN{FS="\t"; OFS="\t"} {if ($6 > 0.05) print $0}' | cut -f 1,2 | sed 1d > indiv.exclu

#Throw out any marker == 0% call rate, which is 100 
cat $RAW_MISSING_DIR/clean.lmiss | awk 'BEGIN{FS="\t"; OFS="\t"} {if ($5 == 1) print $0}' | cut -f 2 > marker.exclu

plink --bfile $INPUT_STEM --remove indiv.exclu --exclude marker.exclu --make-bed --out plat_qc

popd
