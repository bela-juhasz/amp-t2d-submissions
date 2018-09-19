# Open haps file from shapeit. get largest co-ordinate. divide up by megabases i.e 1 5MB, 5MB+1 ... larg(co-ord)
# split up into Chromosomes

import sys, subprocess

#param = sys.argv
#batch = int(param[1]) # where arg is number of chromosomes to run

#bsub = "bsub " + "-J '/nfs/ega/private/ega/work/declan/pipeline_test/bsub_logs/" +str(i) + "_" + str(j) + "' " +" -o" + " '/nfs/ega/private/ega/work/declan/pipeline_test/bsub_logs/"+ str(i) +"_" + str(j) + ".out'" + "-e '/nfs/ega/private/ega/work/declan/pipeline_test/bsub_logs/" +str(i) + "_" + str(j) + ".err'" + "-q analysis-rh7 -M 50000 -R 'rusage[mem=25000]', -R 'span[hosts=1]' "
count = 0

outfile = open("bsub.sh","w")

outfile.write("#!/bin/bash" + "\n" + "\n" + "source 1_Source.sh" + "\n" + "mkdir -p impute2" + "\n" + "\n")

for i in range(1,24):
        print("loading Chromosome " + str(i))
        myfile = open("phased/phased.chr" + str(i) +".haps")
        raw = myfile.readlines()[-1]  # store last line as inputs are ordered (should be anyway)
        myfile.close()
        max_loc = raw.split(" ")[2]
        for j in range(1, (int(max_loc) + 1000000), 6000000):
                if i == 23 :
			Impute2 = "impute2 -chrX -use_prephased_g "
                	bsub = "bsub " + "-J 'bsub_logs/Chr_" +str(i) + "_" + str(j) + "' " +" -o" + " 'bsub_logs/Chr_"+ str(i) +"_" + str(j) + ".out'" + " -e 'bsub_logs/Chr_" +str(i) + "_" + str(j) + ".err'" + " -q analysis-rh7 -M 50000 -R 'rusage[mem=25000]', -R 'span[hosts=1]' "
			refs = "-h $Ref/1000GP_Phase3_chr" + str(i) + ".hap.gz "
              		legend  = "-l $Ref/1000GP_Phase3_chr" + str(i) + ".legend.gz "
                	gmap = "-m $Ref/genetic_map_chr" + str(i) + "_combined_b37.txt "
                	coord = "-int " + str(j) + " " + str(int(j + 6000000))
                	kwn_haps = " -known_haps_g phased/phased.chr" + str(i) + ".haps "
			samp = "-sample_g phased/phased.chr" + str(i) + ".sample "
			out = "-o_gz -o impute2/Chr" + str(i) + "/Chr" + str(i) + "_"+ str(j) + "_" + str(int(j + 6000000)) + ".imp "
			count = count + 1
			imput = bsub + Impute2 + refs + legend + gmap + coord + kwn_haps + samp + out + "-phase" + "\n"
			outfile.write(imput)
                #subprocess.call(["./bsub.sh", imput], shell=True)
		else:
			Impute2 = "impute2 -use_prephased_g "
                        bsub = "bsub " + "-J 'bsub_logs/Chr_" +str(i) + "_" + str(j) + "' " +" -o" + " 'bsub_logs/Chr_"+ str(i) +"_" + str(j) + ".out'" + " -e 'bsub_logs/Chr_" +str(i) + "_" + str(j) + ".err'" + " -q analysis-rh7 -M 50000 -R 'rusage[mem=25000]', -R 'span[hosts=1]' "
                        refs = "-h $Ref/1000GP_Phase3_chr" + str(i) + ".hap.gz "
                        legend  = "-l $Ref/1000GP_Phase3_chr" + str(i) + ".legend.gz "
                        gmap = "-m $Ref/genetic_map_chr" + str(i) + "_combined_b37.txt "
                        coord = "-int " + str(j) + " " + str(int(j + 6000000))
                        kwn_haps = " -known_haps_g phased/phased.chr" + str(i) + ".haps "
                        samp = "-sample_g phased/phased.chr" + str(i) + ".sample "
                        out = "-o_gz -o impute2/Chr" + str(i) + "/Chr" + str(i) + "_"+ str(j) + "_" + str(int(j + 6000000)) + ".imp "
                        count = count + 1
                        imput = bsub + Impute2 + refs + legend + gmap + coord + kwn_haps + samp + out + "-phase" + "\n"
                        outfile.write(imput)

outfile.close()

