#!/bin/bash
#Subscript for finding the raw missingness of the data
WORKSPACE=$1
SCRIPT_DIR=$2
INPUT_STEM=$3

mkdir -p $WORKSPACE
pushd $WORKSPACE

plink --bfile $INPUT_STEM --missing --out raw

#Create clean copies of the reports
cat raw.imiss | sh $SCRIPT_DIR/clean_plink_report.sh > clean.imiss
cat raw.lmiss | sh $SCRIPT_DIR/clean_plink_report.sh > clean.lmiss

#Create a report of individuals, ordered by id
cat clean.imiss | cut -f 2,6 | sed 1d | sort -k 1,1 > sorted.imiss

#Create series of exclusions sets at different missingness cutoffs
#the standard five bins, we can decide which to use after the plotting
cat sorted.imiss | awk 'BEGIN{FS="\t"; OFS="\t";} {if ($2 > 0.05) print $1}' | sort -k 1,1 > gt_5pc.indiv
cat sorted.imiss | awk 'BEGIN{FS="\t"; OFS="\t";} {if ($2 > 0.04) print $1}' | sort -k 1,1 > gt_4pc.indiv
cat sorted.imiss | awk 'BEGIN{FS="\t"; OFS="\t";} {if ($2 > 0.03) print $1}' | sort -k 1,1 > gt_3pc.indiv
cat sorted.imiss | awk 'BEGIN{FS="\t"; OFS="\t";} {if ($2 > 0.02) print $1}' | sort -k 1,1 > gt_2pc.indiv
cat sorted.imiss | awk 'BEGIN{FS="\t"; OFS="\t";} {if ($2 > 0.01) print $1}' | sort -k 1,1 > gt_1pc.indiv

popd
