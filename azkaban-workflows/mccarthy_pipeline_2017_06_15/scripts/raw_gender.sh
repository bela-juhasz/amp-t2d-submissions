#!/bin/bash
#Subscript for isolating gender mismatched, etc

WORKSPACE=$1
SCRIPT_DIR=$2
INPUT_STEM=$3

mkdir -p $WORKSPACE
pushd $WORKSPACE

# Gender should not be applied by default, is carried in a separate gender file
plink --bfile $INPUT_STEM --update-sex $INPUT_STEM.gender --make-bed --out 01.with_gender

plink --bfile 01.with_gender --check-sex --out 02.sex_check

cat 02.sex_check.sexcheck | sh $SCRIPT_DIR/clean_plink_report.sh > 03.clean.sexcheck

cat 03.clean.sexcheck | awk 'BEGIN{FS="\t"; OFS="\t";} {if ($5 == "PROBLEM") print $2}' | sort -u > 04.problem.indiv

popd
