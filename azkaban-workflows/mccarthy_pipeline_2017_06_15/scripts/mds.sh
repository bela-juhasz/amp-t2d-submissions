#!/bin/bash
#Subscript for running an MDS from the merged reference data
WORKSPACE=$1
SCRIPT_DIR=$2
REF_MERGE_DIR=$3
RAW_MISSING_DIR=$4

mkdir -p $WORKSPACE
pushd $WORKSPACE

#Run the IBD
plink --bfile $REF_MERGE_DIR/05.merge --Z-genome --out 01.genome

#Run the MDS
plink --bfile $REF_MERGE_DIR/05.merge --read-genome 01.genome.genome.gz --cluster --mds-plot 10 --out 02.raw

#Clean the MDS
cat 02.raw.mds | sh $SCRIPT_DIR/clean_plink_report.sh > 03.clean.mds

#Create a clean, primary dataset only pihat file
zcat 01.genome.genome.gz | sed 1d | sh $SCRIPT_DIR/clean_plink_report.sh | awk 'BEGIN{FS="\t"; OFS="\t";} {if ($1 == "PRIMARY" && $3 == "PRIMARY" && $10 != 0) print $2, $4, $10}' | gzip -c > 10.internal_only.pihat.gz

#Now create a report that captures the overall number of pairs
zcat 10.internal_only.pihat.gz | awk '
	BEGIN{FS="\t"; OFS="\t"; for (i = 0; i < 10; i++) {a[i]=0}} 
	{	x = int($3 * 10) / 1;
		if (x == 10) x -= 1;
		a[x] += 1;
	}
	END{for(i in a)print i"\t<"((i + 1) / 10)"\t"a[i];}' | sort -k 1,1 -n > 11.pihats.grouped
	
#Now do a report of those that are >= 0.9 (identical) and >= 0.4 (1st degree relation)
zcat 10.internal_only.pihat.gz | awk 'BEGIN{FS="\t"; OFS="\t";} {if ($3 >= 0.9) print $0}' > 12.pihat.gte_0_9
zcat 10.internal_only.pihat.gz | awk 'BEGIN{FS="\t"; OFS="\t";} {if ($3 >= 0.4) print $0}' > 12.pihat.gte_0_4

#Now attach missingness to all the duplicates, so that we can identify which is the better of each pair!
cat 12.pihat.gte_0_9 | cut -f 1 | awk 'BEGIN{FS="\t"; OFS="\t";} {print $0, NR}' | sort -k 1,1 | join - $RAW_MISSING_DIR/sorted.imiss | sort -k 2,2 -n > 13.pihat.gte_0_9.col1
cat 12.pihat.gte_0_9 | cut -f 2 | awk 'BEGIN{FS="\t"; OFS="\t";} {print $0, NR}' | sort -k 1,1 | join - $RAW_MISSING_DIR/sorted.imiss | sort -k 2,2 -n > 13.pihat.gte_0_9.col2
cat 12.pihat.gte_0_4 | cut -f 1 | awk 'BEGIN{FS="\t"; OFS="\t";} {print $0, NR}' | sort -k 1,1 | join - $RAW_MISSING_DIR/sorted.imiss | sort -k 2,2 -n > 13.pihat.gte_0_4.col1
cat 12.pihat.gte_0_4 | cut -f 2 | awk 'BEGIN{FS="\t"; OFS="\t";} {print $0, NR}' | sort -k 1,1 | join - $RAW_MISSING_DIR/sorted.imiss | sort -k 2,2 -n > 13.pihat.gte_0_4.col2

paste 13.pihat.gte_0_9.col1 13.pihat.gte_0_9.col2 > 14.pihat.gte_0_9.plus_imiss
paste 13.pihat.gte_0_4.col1 13.pihat.gte_0_4.col2 > 14.pihat.gte_0_4.plus_imiss

paste 14.pihat.gte_0_9.plus_imiss | sh $SCRIPT_DIR/clean_plink_report.sh | awk '
	BEGIN{FS="\t"; OFS="\t";} 
	{if ($3 <= $6) {print $1,$3,$4,$6} else {print $4,$6,$1,$3}}' > 15.pihat.gte_0_9.imiss_ordered

paste 14.pihat.gte_0_4.plus_imiss | sh $SCRIPT_DIR/clean_plink_report.sh | awk '
	BEGIN{FS="\t"; OFS="\t";} 
	{if ($3 <= $6) {print $1,$3,$4,$6} else {print $4,$6,$1,$3}}' > 15.pihat.gte_0_4.imiss_ordered


popd
