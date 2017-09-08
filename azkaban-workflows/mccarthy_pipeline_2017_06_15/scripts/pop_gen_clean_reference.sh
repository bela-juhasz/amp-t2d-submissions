#!/bin/bash
#Clean the reference data before merging
WORKSPACE=$1
SCRIPT_DIR=$2
REF_STEM=$3

mkdir -p $WORKSPACE
pushd $WORKSPACE

#1KG is sequence data, so missingnesses can be higher, so we don't put a harsh gt threshold on
plink --bfile $REF_STEM --maf 0.01 --geno 0.1 --make-bed --out 00.clean

#Remove palindromic markers
cat 00.clean.bim | sh $SCRIPT_DIR/clean_plink_report.sh | sh $SCRIPT_DIR/remove_palindromic.sh > 01.palin.markers
plink --bfile 00.clean --exclude 01.palin.markers --make-bed --out 01.super_clean

popd
