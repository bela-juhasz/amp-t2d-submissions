#!/bin/bash
#Subscript to output exclusion reports

WORKSPACE=$1
EXCLU_SET_DIR=$2

mkdir -p $WORKSPACE
pushd $WORKSPACE

#Merge all the exclusion lists into single lists
cat $EXCLU_SET_DIR/*.indiv | sort -u > indiv.exclu
cat $EXCLU_SET_DIR/*.marker | sort -u > marker.exclu

popd
