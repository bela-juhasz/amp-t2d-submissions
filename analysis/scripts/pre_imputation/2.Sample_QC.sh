#!/bin/bash
#BSUB -J OUT_2
#BSUB -n 1 # request 8 cores
#BSUB -o "bsub_logs/OUT_2.out"
#BSUB -M 5000
#BSUB -e "bsub_logs/OUT_2.err"
#BSUB -R "rusage[mem=5000]" # request 2000MB per job slot, or 16000MB total
#BSUB -R "span[hosts=1]"
#BSUB -L /bin/bash
#BSUB -q "analysis-rh7"

source ./1_Source.sh

###############################################################################################################################################
#### Sample level QC ensure no filters have been applied to the data already esp maf.
###############################################################################################################################################

## remove ambu=iguous sex samples. G1K gives all problems may be better to use sex derived from snp or filter last column >.8 male <0.2 female
plink $INPUT_TYPE $IN --allow-no-sex --allow-extra-chr --chr 1-22,X --check-sex --mind $MIND --make-bed --out temp_t2d

## heterozygosity Het = (N(NM) - O(Hom))/N(M) Giant recommends excluding indivs with Het > med + (3*IQR)
plink --bfile temp_t2d --geno $GENO --hwe $HWE midp --het --make-bed  --out temp_t2d_2

## Remove cryptic individuals
plink --bfile temp_t2d_2 --indep-pairwise 500 50 0.2 --out prune
plink --bfile temp_t2d_2 --extract prune.prune.in --freq --make-bed --out pruned
plink --bfile pruned --genome --min 0.185 --missing --make-bed --out temp_t2d_3

# remove duplicates
plink --bfile temp_t2d_3 --list-duplicate-vars --out exclude
grep -v CHR exclude.dupvar > exclude1.dupvar
plink --bfile temp_t2d_3 --exclude exclude1.dupvar --check-sex --het --make-bed --out t2d

