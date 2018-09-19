#!/bin/sh
#BSUB -J 1b
#BSUB -n 4 # request 8 cores
#BSUB -o "bsub_logs/1b.out"
#BSUB -M 16000
#BSUB -e "bsub_logs/1b.err"
#BSUB -R "rusage[mem=16000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"
#A script for updating a binary ped file using one of Will's strand files
#NRR 17th Jan 2012

#V2 13th Feb 2012. Added code to retain only SNPs in the strand file

#Required parameters:
#1. The original bed stem (not including file extension suffix)
#2. The strand file to apply
#3. The new stem for output
#Result: A new bed file (etc) using the new stem

#Required parameters:
#1. The original bed stem (not including file extension suffix)
#2. The strand file to apply
#3. The new stem for output
#Result: A new bed file (etc) using the new stem

#Added by M. Forest to match the plink version we have
PLINK_EXEC=`which plink`

source ./1_Source.sh

#Unpack the parameters into labelled variables
stem=$INPUT
strand_file=$CHIP".strand"
outstem="updated"

echo Input stem is $stem
echo Strand file is $strand_file
echo Output stem is $outstem

#Cut the strand file into a series of Plink slices
chr_file=$strand_file.chr
pos_file=$strand_file.pos
flip_file=$strand_file.flip
cat $strand_file | cut -f 1,2 > $chr_file
cat $strand_file | cut -f 1,3 > $pos_file
cat $strand_file | awk '{if ($5=="-") print $0}' | cut -f 1 > $flip_file

#Because Plink only allows you to update one attribute at a time, we need lots of temp
#Plink files
temp_prefix=TEMP_FILE_XX72262628_
temp1=$temp_prefix"1"
temp2=$temp_prefix"2"
temp3=$temp_prefix"3"

#1. Apply the chr
plink --allow-extra-chr --allow-no-sex --bfile $stem --update-chr $chr_file --make-bed --out $temp1
#2. Apply the pos
plink --allow-no-sex --allow-extra-chr --bfile $temp1 --update-map $pos_file --make-bed --out $temp2
#3. Apply the flip
plink --allow-no-sex --allow-extra-chr --bfile $temp2 --flip $flip_file --make-bed --out $temp3
#4. Extract the SNPs in the pos file, we don't want SNPs that aren't in the strand file
plink --allow-no-sex --allow-extra-chr --bfile $temp3 --extract $pos_file --make-bed --out $outstem

#Now delete any temporary artefacts produced
rm -f $temp_prefix*

