#!/bin/bash
#Run a rough internal IBD on the raw samples so that we can detect cross-contamination
WORKSPACE=$1
SCRIPT_DIR=$2
INPUT_STEM=$3
COMPLEX_REGIONS_PATH=$4

mkdir -p $WORKSPACE
pushd $WORKSPACE

#This is a copy of pop_gen_clean and perhaps should be subscripted!!

#Take the aligned data and remove SNPs with >1% missing, <1% maf, <0.0001 HWE
plink --bfile $INPUT_STEM --maf 0.01 --geno 0.01 --hwe 0.0001 --make-bed --out 00.super_clean

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

#Now run an IBD looking at GT 0.7 PIHAT and above
plink --bfile 04.pruned --Z-genome --min 0.4 --out 05.genome

#Clean the IBD
zcat 05.genome.genome.gz | sh $SCRIPT_DIR/clean_plink_report.sh | cut -f 2,4,10 | gzip -c > 06.clean.ibd.gz

#Now create a report that captures the overall number of pairs
zcat 06.clean.ibd | awk '
	BEGIN{FS="\t"; OFS="\t"; for (i = 0; i < 10; i++) {a[i]=0}} 
	{	x = int($3 * 10) / 1;
		if (x == 10) x -= 1;
		a[x] += 1;
	}
	END{for(i in a)print i"\t<"((i + 1) / 10)"\t"a[i];}' | sort -k 1,1 -n > 07.pihats.grouped

popd
