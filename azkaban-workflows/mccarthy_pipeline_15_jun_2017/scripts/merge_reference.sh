#!/bin/bash
#Subscript for running an IBD and MDS plot
WORKSPACE=$1
REF_CLEAN_DIR=$2
CHR_POS_DIR=$3

mkdir -p $WORKSPACE
pushd $WORKSPACE

echo Working Directory is `pwd`

cat $REF_CLEAN_DIR/01.super_clean.bim | cut -f 2,5,6 | sort -k 1,1 > 01.int_bim_sorted
cat $CHR_POS_DIR/01.chr_pos.bim | cut -f 2,5,6 | sort -k 1,1 > 01.ref_bim_sorted

join 01.int_bim_sorted 01.ref_bim_sorted > 02.join

#Remove any markers where the alleles do not agree
cat 02.join | awk '{if ((($2 != $4) && ($2 != $5)) || (($3 != $4) && ($3 != $5))) print $0}' | cut -f 1 > 03.incompatible_markers
cat 02.join | awk '{if (!((($2 != $4) && ($2 != $5)) || (($3 != $4) && ($3 != $5)))) print $0}' | cut -f 1 > 03.overlap_markers

#Now create the overlapping sets
plink --bfile $REF_CLEAN_DIR/01.super_clean --extract 03.overlap_markers --make-bed --out 04.int_overlap
plink --bfile $CHR_POS_DIR/01.chr_pos --extract 03.overlap_markers --make-bed --out 04.ref_overlap
plink --bfile 04.int_overlap --bmerge 04.ref_overlap.bed 04.ref_overlap.bim 04.ref_overlap.fam --make-bed --out 05.merge

popd
