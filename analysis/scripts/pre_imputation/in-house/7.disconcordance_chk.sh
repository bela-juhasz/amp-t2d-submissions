#!/bin/bash
#BSUB -J 7_OUT
#BSUB -n 4 # request 8 cores
#BSUB -o "bsub_logs/7_OUT.out"
#BSUB -M 16000
#BSUB -e "bsub_logs/7_OUT.err"
#BSUB -R "rusage[mem=16000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"

source ./1_Source.sh

echo "Finding variants in disconcordance to reference"
## loop over chromosomes and find variants not in alignment with Reference
for i in {1..23}; do
        if ${i} == 23; then
                shapeit -check --chrX --input-bed GWAS_data/myGwasData.chr${i} \
                --input-map $Ref/genetic_map_chr${i}_combined_b37.txt \
                --input-ref $Ref/1000GP_Phase3_chr10.hap.gz $Ref/1000GP_Phase3_chr10.legend.gz $Ref/1000GP_Phase3.sample \
                --output-log disconcordant/${i}
        else
                shapeit -check --input-bed GWAS_data/myGwasData.chr${i} \
                --input-map $Ref/genetic_map_chr${i}_combined_b37.txt \
                --input-ref $Ref/1000GP_Phase3_chr10.hap.gz $Ref/1000GP_Phase3_chr10.legend.gz $Ref/1000GP_Phase3.sample \
                --output-log disconcordant/${i}
        fi
done

#write levels of unalignment to disconcordant/log.txt

for j in {1..23}; do
        grep "Strand" disconcordant/${j}.snp.strand | awk '{print $4}' > disconcordant/chr${j}_disc_snps.txt;
        count_dis=$(wc disconcordant/chr${j}_disc_snps.txt | awk '{print $1}');
        tot_snps=$(wc GWAS_data/myGwasData.chr${j}.bim | awk '{print $1}');
        percent=$(awk "BEGIN { pc=100*${count_dis}/${tot_snps}; i=int(pc); print (pc-i<0.5)?i:i+1 }");
        echo "Chromosome ${j}: ${count_dis} out of ${tot_snps} were disconcordant to reference panel: $percent percent" >> disconcordant/Counts_log.txt;
done

# removal of variants not in alignment
for chr in {1..23}; do
        plink --bfile GWAS_data/myGwasData.chr${chr} --exclude disconcordant/chr${chr}_disc_snps.txt --make-bed --out GWAS_data/aligned/Chr${chr}.align;
done

rm *.nosex
