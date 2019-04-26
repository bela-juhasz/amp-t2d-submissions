#!/bin/bash
#BSUB -J "firstpassfilt"
#BSUB -n 2 # request 8 cores
#BSUB -o "filt.o"
#BSUB -M 16000
#BSUB -e "filt.e"
#BSUB -R "rusage[mem=7000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"

bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_1.o -e info_1.e "bcftools filter -i 'R2<1 && R2>0.9' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_1.vcf.gz"
bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_2.o -e info_2.e "bcftools filter -i 'R2<0.9 && R2>0.8' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_.2.vcf.gz"
bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_3.o -e info_3.e "bcftools filter -i 'R2<0.8 && R2>0.7' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_.3.vcf.gz"
bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_4.o -e info_4.e "bcftools filter -i 'R2<0.7 && R2>0.6' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_.4.vcf.gz"
bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_5.o -e info_5.e "bcftools filter -i 'R2<0.6 && R2>0.5' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_.5.vcf.gz"
bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_6.o -e info_6.e "bcftools filter -i 'R2<0.5 && R2>0.4' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_.6.vcf.gz"
bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_7.o -e info_7.e "bcftools filter -i 'R2<0.4 && R2>0.3' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_.7.vcf.gz"
bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_8.o -e info_8.e "bcftools filter -i 'R2<0.3 && R2>0.2' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_.8.vcf.gz"
bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_9.o -e info_9.e "bcftools filter -i 'R2<0.2 && R2>0.1' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_.9.vcf.gz"
bsub -R 'select[mem>2000] rusage[mem=2000]' -M2000 -q analysis-rh7 -o info_10.o -e info_10.e "bcftools filter -i 'R2<0.1 && R2>0.0' ../Hoorn_v2.GP.dropped.vcf.gz -Oz -o Hoorn_v2_INFO_.10.vcf.gz"