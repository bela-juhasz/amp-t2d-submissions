#!/bin/bash
#Subscript to draw together exclusion sets for individuals and markers
WORKSPACE=$1
PLATFORM_QC_DIR=$2
RAW_MISSING_DIR=$3
RAW_GENDER_DIR=$4

mkdir -p $WORKSPACE
pushd $WORKSPACE

#Collect the platform exclusions
cat $PLATFORM_QC_DIR/indiv.exclu | sort -u > PLATFORM.indiv
cat $PLATFORM_QC_DIR/marker.exclu | sort -u > PLATFORM.marker

#Collect the missingness exclusions
cat $RAW_MISSING_DIR/gt_3pc.indiv | sort -u > MISSINGNESS.indiv

#Collect the gender exclusions
cat $RAW_GENDER_DIR/04.problem.indiv | sort -u > GENDER.indiv

popd
