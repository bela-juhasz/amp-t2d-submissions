#!/bin/bash
####
##
##
## Form Jason Flannick. Extracts Anubhas 243 significant T2D variants and checks that the REF/ALT are aligned and flips the vcf is not. 
## My understanding is that the burden code that drives the GRS will be updated at some point to assign weights on the fly but until then this needs to be done
####
(tabix -H $1;for i in `cut -f1-2 $2 | awk '{print $1":"$2"-"$2}'`; do tabix $1 $i; done) | bgzip -c > GRS.vcf.gz

zcat GRS.vcf.gz | cat $2 - | gawk -F"\t" -v OFS="\t" 'NF == 4 {key=$1":"$2; r[key]=$3; o[key]=$4} /#/ {print} !/#/ && NF > 4 {snp=$1":"$2; if (r[snp] == $5 && o[snp]=$4) {print} else if (r[snp] == $4 && o[snp]=$5) {t=$4; $4=$5; $5=t; line=gensub(/1([\|\/])1/, "9\\19", "g"); line=gensub(/0([\|\/])0/, "1\\11", "g",line); line=gensub(/9([\|\/])9/, "0\\10", "g",line); print line}}' | bgzip > GRS_fg_ready.vcf.gz;

zcat GRS_fg_ready.vcf.gz | python ~/amp-t2d-submissions/foghorn_python/foghorn/foghorn_main.py -o Platform -GT

bgzip -c Platform_genotypes.cvcf > GRS.cvcf.gz

tabix -p vcf GRS.cvcf.gz
