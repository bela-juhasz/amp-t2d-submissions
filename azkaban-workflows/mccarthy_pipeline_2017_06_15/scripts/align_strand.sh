#!/bin/bash
#Subscript for aligning to the given strand file

WORKSPACE=$1
PLATFORM_QC_DIR=$2

mkdir -p $WORKSPACE

#Just call the classic update_build script
#sh $SCRIPT_DIR/update_build.sh $WORKING_DIR/$PLATFORM_QC_DIR/plat_qc $STRAND_PATH $WORKSPACE

#Or if already, then mock it!!
plink --bfile $PLATFORM_QC_DIR/plat_qc --make-bed --out $WORKSPACE/aligned
