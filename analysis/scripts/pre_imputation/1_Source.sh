#!/bin/bash

## Depending on input type shapeit and impute will have to be changed independently. If sex is available load to plink format and do not recode. 


# Create Directories

mkdir -p bsub_logs
mkdir -p logs
mkdir -p QC
mkdir -p GWAS_data/aligned
mkdir -p strand_checkerout
mkdir -p disconcordant
mkdir -p phased


# set paths
# Refs 1000G maps and haps for impute2 - need to get HRC access also
Ref="/nfs/ega/private/amp/T2D/submissions/1000GP_Phase3"
REFlegend="/nfs/ega/private/amp/T2D/submissions/1000GP_Phase3/1000GP_Phase3_combined.legend" # This is for perl script
DATA="./GWAS_data/aligned/"
CHIP="/nfs/ega/private/amp/T2D/submissions/1000GP_Phase3/chips/Affy-NSP-STY-b37.58-v4"
POS="/nfs/ega/private/amp/T2D/submissions/1000GP_Phase3/checkPositions.awk"

# Input type & input
INPUT_TYPE="--bfile" #"--vcf", "--file"
INPUT="tplink/ALL" # --vcf will contain .vcf whereas plink files will only contain the handle
IN=$(pwd)/updated # take cwd merge with update_build

# Thresholds
MAF=0.01
GENO=0.02
MIND=0.1
HWE=0.000001

# path to tools
plink="~/bin/plink"
shapeit="~/bin/shapeit"
impute2="~/bin/impute2" 


# perl script super population
POP="EUR"


