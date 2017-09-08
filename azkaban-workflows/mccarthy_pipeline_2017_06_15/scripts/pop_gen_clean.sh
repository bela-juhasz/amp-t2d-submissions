#!/bin/bash
#Super clean the internal dataset ready for genome runs, MDS plotting, etc
WORKSPACE=$1
SCRIPT_DIR=$2
COMPLEX_REGIONS_PATH=$3
STRAND_ALIGN_DIR=$4

mkdir -p $WORKSPACE
pushd $WORKSPACE

#Take the aligned data and remove SNPs with >1% missing, <1% maf, <0.0001 HWE
plink --bfile $STRAND_ALIGN_DIR/aligned --maf 0.01 --geno 0.01 --hwe 0.0001 --make-bed --out 00.super_clean

#Remove non-autosomal markers and palindromic markers
cat 00.super_clean.bim | sh $SCRIPT_DIR/clean_plink_report.sh | grep -P "^0|^2[3456]" > 01.non_auto.markers
cat 00.super_clean.bim | sh $SCRIPT_DIR/clean_plink_report.sh | sh $SCRIPT_DIR/remove_palindromic.sh > 01.palin.markers
cat 01.non_auto.markers 01.palin.markers | sort -u > 01.exclu.markers
plink --bfile 00.super_clean --exclude 01.exclu.markers --make-bed --out 01.auto_no_palins

#Remove any markers within the COMPLEX REGIONS / HLA, etc
plink --bfile 01.auto_no_palins --exclude range $COMPLEX_REGIONS_PATH --make-bed --out 02.no_complex

#Now LD prune
plink --bfile 02.no_complex --indep 50 5 1.25 --out 03.ld
plink --bfile 02.no_complex -extract 03.ld.prune.in --make-bed --out 04.pruned

popd
