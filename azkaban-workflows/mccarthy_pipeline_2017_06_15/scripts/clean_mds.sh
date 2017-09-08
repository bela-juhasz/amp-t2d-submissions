#!/bin/bash
#Subscript running the final MDS plot of clean data, exclusions applied
WORKSPACE=$WORKING_DIR/$CLEAN_MDS_DIR
mkdir -p $WORKSPACE
pushd $WORKSPACE

#Create a new clean set, from the clean popgen files, not the chr_pos ones for merging!!
plink --bfile $POP_GEN_CLEAN_DIR/04.pruned --remove $EXCLU_SET_DIR/total_exclusions.fam --make-bed --out 00.mds_clean

#Run the IBD
plink --bfile 00.mds_clean --Z-genome --out 01.genome

#Run the MDS
plink --bfile 00.mds_clean --read-genome 01.genome.genome.gz --cluster --mds-plot 10 --out 02.raw

#Clean the MDS
cat 02.raw.mds | sh $SCRIPT_DIR/clean_plink_report.sh > 03.clean.mds

popd
