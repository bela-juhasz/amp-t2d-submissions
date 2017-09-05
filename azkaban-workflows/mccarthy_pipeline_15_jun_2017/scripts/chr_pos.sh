#!/bin/bash
#Subscript for renaming markers for merging with external data (1KG, etc)
WORKSPACE=$1
SCRIPT_DIR=$2
POP_GEN_CLEAN_DIR=$3

mkdir -p $WORKSPACE
pushd $WORKSPACE

#Turn all marker names into CHR_POS format, for merging
cat $POP_GEN_CLEAN_DIR/04.pruned.bim | sh $SCRIPT_DIR/clean_plink_report.sh | awk 'BEGIN{FS="\t"; OFS="\t";} {print $2, $1"_"$4}' > 01.marker.remap

#Change all the FIDs, so that we can easily recognize our primary dataset from the reference dataset
cat $POP_GEN_CLEAN_DIR/04.pruned.fam | sh $SCRIPT_DIR/clean_plink_report.sh | awk 'BEGIN{FS="\t"; OFS="\t";} {print $1, $2, "PRIMARY", $2}' > 01.indiv.remap

plink --bfile $POP_GEN_CLEAN_DIR/04.pruned --update-name 01.marker.remap --update-ids 01.indiv.remap --make-bed --out 01.chr_pos

popd
