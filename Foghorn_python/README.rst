VCF compression tool 
`````````````````````

This python tool converts vcf file into cVCF format as used by the AMP-T2D knowledge portals genetic analysis interactive tool (GAIT) 
To use, stream a vcf to the tool with with an outfile flag and compression type

zcat inVCF.vcf.gz | python foghorn_python.py -o outfile -GT[DS]

The GT flag implements the genotype compression algorithm 
The DS flag implements the gene dosage compression algorithm
