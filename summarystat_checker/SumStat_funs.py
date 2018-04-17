import gzip, math, sys, pysam, hashlib
from gzopen import gzopen 

#################
# global Variables
#################

def check_tool(line): # set global variables depending on the hash of the header. rvtests and raremetalworker are similar but not identical
	global AF
	global BETA
	global N_ref
	global het
	global N_alt
	global samsize
	global md5
        if str(hashlib.md5(line.strip("\n")).hexdigest()) == "0433803d1fb0379712714139be0c9194": # make this the md5 for rvtests header
		md5 = "0433803d1fb0379712714139be0c9194"
		AF = 5
		BETA = 14
		N_ref = 9
		het = 10
		N_alt = 11
		samsize = 4
		return "md5 = ", md5, "AF= ",AF, "BETA= ", BETA, "Ref_all = ", N_ref, "het_all = ", het, " Alt_all = ", N_alt," Sample_size index= ", samsize
	elif hashlib.md5(line.strip("\n")).hexdigest() == "5a91ec7be068aa0f2ae6fa13112cd487": # this the header for metalworker 
		md5 = "5a91ec7be068aa0f2ae6fa13112cd487"
		AF = 6
		BETA = 15
		N_ref = 10
		het = 11
		N_alt = 12
		samsize = 4
        	return "md5 = ", md5,AF, "BETA= ", BETA, "Ref_all = ", N_ref, "het_all = ", het, " Alt_all = ", N_alt," Sample_size index= ", samsize
	else:#  -input from command line eventually will allow any tool to be used provided global variables are provided. Can switch to HWE estimates if no genotype counts.
		return
#############
### Functions
##############

def MAC(line): # minor allele count uses the smaller homozygous group to determine the minor allele count
	if int(line[int(N_ref)]) < int(line[N_alt]):
		return str(int(line[het]) +(2 * int(line[N_ref])))
	else:
		return str(int(line[het]) +(2 * int(line[N_alt])))
def EAC(line): # effect allele count  takes genotype counts
	EAC = str(int(line[het]) +(2 * int(line[N_alt])))
	return EAC

#def MAC_hwe(line): # this can be used when genotype counts are not available, use HWE to infer counts. susceptible to high heterozygosity may be able to adjust with Fst but not sure
#	MAChwe = str((line[AF] * (float(line[16])**2)) + (line[4] * ((2* (float(line[16]) * (1 - float(line[16])))))))
#	return MAChwe

def monomorphic_filter(line): # remove sites with no variation. These shouldnt appear in a summary stat file. Extend issue
        if ((int(line[N_ref] and line[het])) == 0 or (line[het] and line[N_alt] == 0) or (line[N_alt] and line[N_ref] == 0)):
                return True
        else:
                return False
def MAF(line): # MAF uses given EAF
	if float(line[AF]) > 0.5:
		return str((1 - float(line[AF]))) # MAF
	else:
		return str(line[AF])

# Beta -> OR raremetalworker
def Beta2ORinvert(line, md5): # Beta to OR where the principal of "invariance of the odds ratio" is used to calculate OR for the non-reference allele. again good qc should eliminate this problem.
	if md5 == "5a91ec7be068aa0f2ae6fa13112cd487":
		k = float(1/float(line[AF])) / float(1- float(line[AF]))
		if float(line[BETA]) < 5: # thresholding at Beta < 5 can be added as a input param, hack to stop wild odds ratios from being entered and causing havoc. need to update the SE also. but not important as portal doesnt use it.
			try:
				OR = math.exp((float(line[BETA]) * k)) # This is for transforming Beta to OR when the ref != ref raremetal and rvtests
				return str(OR)
			except OverflowError:
				OR = "NA"
				return str(OR)
		else:
			return "NA"
	else:
		if float(line[BETA]) < 5:
                        try:
                                OR = math.exp(float(line[BETA])) # This is for transforming Beta to OR when the ref != ref raremetal and rvtests
                                return str(OR)
                        except OverflowError:
                                OR = "NA"
                                return str(OR)
                else:
                        return "NA"


def Beta2OR(line,md5): # standard well aligned dataa
	if md5 == "5a91ec7be068aa0f2ae6fa13112cd487":
		k = float(1/float(line[AF])) / float(1- float(line[AF]))
		if float(line[BETA]) < 5:
			try:
				OR = math.exp(((float(line[BETA]) *-1) * k)) 
				return str(OR)
			except OverflowError:
				OR = "NA"
	        		return str(OR)
		else:
			return "NA"
	else:
		if float(line[BETA]) < 5:
			try:
				OR = math.exp((float(line[BETA]) *-1)) 
               			return str(OR)
			except OverflowError:
				OR = "NA"
				return str(OR)
		else:
			return "NA" 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Rvtests function for Binary traits, change name here and below for quan as well as in the script to call functions

def Rvtests_bin(Sumstat, fasta):
	with gzopen(Sumstat) as stats: # call gzoopen to open file or file.zip on the fly
		OUT = open(str(Sumstat.split("/")[-1] + ".Tidy"),"w")  # output
		genome = pysam.Fastafile(fasta) # load fasta file only needs to be done once as it writes the index
		count = 0 # number of variants
		count_mm = 0 #mismatches
		count_m = 0 #matches
		for line in stats:
			if line.startswith("##") or line.startswith("#G"): # rv tests has drivel at the start and the genomic lambda may be the last line
				continue
			elif line.startswith("CHROM") or line.startswith("#CHROM"): # This part will be used to inform how the transformations happen based on what package is used. ie different headers identify different packages
				check_tool(line)
				li_pos = line.strip().split("\t")
				li_pos.append("MAF_PH")
				li_pos.append("MAC_PH")
				li_pos.append("EAC_PH")
				li_pos.append("EAF_PH")
				li_pos[BETA] = "OR"
				li_pos.append("\n")
				OUT.write("\t".join(li_pos)) # write out
			else:
				li_pos = line.strip("\n").split("\t")
				bp_pos = li_pos[1] #base position
				chr_n = li_pos[0] #chr number
				stat_ref = li_pos[2] # reference or non effect allele
				if ((chr_n.isdigit() and int(chr_n) == 23) or chr_n == "X") and monomorphic_filter(li_pos) is False: # for the X chromosome.
					chr_n = "X" # rename chr23
					gen_ref = genome.fetch(chr_n,int(bp_pos)-1,int(bp_pos)) ## query the reference genome using pysam.
					if stat_ref != gen_ref: # output statistics for switched Ref/Alt
						count_mm = count_mm + 1 # update mismatch counter
						li_pos[2] = gen_ref # swap references
						li_pos[3] = stat_ref # swap alternative
						li_pos[BETA] = str(Beta2ORinvert(li_pos,md5)) # Update BETA to OR
						li_pos.append(MAF(li_pos)) # update MAF
						li_pos.append(MAC(li_pos)) # update MAC
						li_pos[N_ref], li_pos[N_alt] = li_pos[N_alt], li_pos[N_ref] # Swap genotype counts when misaligned Important to do this before EAC
						li_pos.append(EAC(li_pos)) # update EAC
						li_pos.append(str((1 - float(li_pos[AF])))) # Update EAF
						li_pos.append("\n") # require
						OUT.write("\t".join(li_pos)) # write to new sumstat file
					elif stat_ref == gen_ref: # Update Statistics where Ref/Alt non switched
						li_pos.append(MAF(li_pos))
						li_pos.append(MAC(li_pos))
						li_pos.append(EAC(li_pos))
						li_pos.append((str(float(li_pos[AF]))))
						li_pos[BETA] = str(Beta2OR(li_pos,md5)) #BETA->OR
						count_m = count_m + 1 # update matches
						li_pos.append("\n")
						OUT.write("\t".join(li_pos))
					else:
						continue
				elif chr_n.isdigit() and int(chr_n) > 23: # for non autosomal & sex chromosomes 
                                	continue
				elif (chr_n.isdigit() and int(chr_n) < 23 ) and monomorphic_filter(li_pos) is False: # This is the body of the computational part all autosomes
					gen_ref = genome.fetch(chr_n,int(bp_pos)-1,int(bp_pos)) # Query reg genome
					if stat_ref != gen_ref:
						count_mm = count_mm + 1
						li_pos[2] = gen_ref # swap references
						li_pos[3] = stat_ref # swap alternatives
						li_pos[BETA] = str(Beta2ORinvert(li_pos,md5))
						li_pos.append(MAF(li_pos))
						li_pos.append(MAC(li_pos))
						li_pos[N_ref], li_pos[N_alt] = li_pos[N_alt], li_pos[N_ref]
						li_pos.append(EAC(li_pos))
						li_pos.append(str(1 - float(li_pos[AF])))
						li_pos.append("\n")
						OUT.write("\t".join(li_pos))
					elif stat_ref == gen_ref:
						li_pos.append(MAF(li_pos))
						li_pos.append(MAC(li_pos))
						li_pos.append(EAC(li_pos))
						li_pos.append((str(float(li_pos[AF]))))
						li_pos[BETA] = str(Beta2OR(li_pos,md5))
						count_m = count_m + 1
						li_pos.append("\n")
						OUT.write("\t".join(li_pos))
					else:
						continue
				else:
					continue
				count = count + 1
		OUT.close()
		return str(count_mm) + " Mismatches: Reference allele is effect allele" + "\n" + str(count_m) + " Matches to reference" + "\n" + str(count) + " Sites checked"

### Rvtests for quantitative traits
def Rvtests_Quan(Sumstat, fasta):
        with gzopen(Sumstat) as stats:
                OUT = open(str(Sumstat.split("/")[-1] + ".Tidy"),"w")
		genome = pysam.Fastafile(fasta) # load and index file only needs to be done once as it writes the index
		count = 0 # testing
		count_mm = 0 #mismatches
		count_m = 0 #matches
                for line in stats:
                        if line.startswith("##")or line.startswith("#G"): # rv tests has drivel at the start
                                continue
                        elif line.startswith("CHROM") or line.startswith("#CHROM"): # This part will be used to inform how the transformations happen based on what package is used. ie different headers identify different packages
                                print check_tool(line)
				li_pos = line.strip("\n").split("\t")
                                li_pos.append("MAF_PH")
                                li_pos.append("MAC_PH")
				li_pos.append("EAC_PH")
                                li_pos.append("EAF_PH")
                                li_pos[BETA] = "BETA"
                                li_pos.append("\n")
                                OUT.write("\t".join(li_pos))
                        else:
                                li_pos = line.strip("\n").split("\t")
                                bp_pos = li_pos[1] #base position
                                chr_n = li_pos[0] #chr number
                                stat_ref = li_pos[2] # reference or non effect allele
                                if ((chr_n.isdigit() and int(chr_n) == 23) or chr_n == "X") and  monomorphic_filter(li_pos) is False: # for the X chromosome Currently using genotype counts to limit rows i.e if a variant is only homozygous for one allele the site is theoretically non informative, Can switch to using 1/2*number of samples this yields the theoretical MAF that can be observed given the data.
                                        chr_n = "X"
                                        gen_ref = genome.fetch(chr_n,int(bp_pos)-1,int(bp_pos)) ## query the reference genome using pysam.
                                        if stat_ref != gen_ref: # output statistics for switched Ref/Alt
                                                count_mm = count_mm + 1
                                                li_pos[2] = gen_ref # swap references
                                                li_pos[3] = stat_ref # swap alternative
                                                li_pos[BETA] = float(li_pos[BETA]) * -1 # Update BETA
                                                li_pos.append(MAF(li_pos))
						li_pos.append(MAC(li_pos))
                                                li_pos[N_alt], li_pos[N_ref] = li_pos[N_ref], li_pos[N_alt]
						li_pos.append(EAC(li_pos))#update MAC
                                                li_pos.append(str((1 - float(li_pos[AF])))) # Update EAF
                                                li_pos.append("\n") # require
                                                OUT.write("\t".join(li_pos)) # write to new sumstat file
                                        elif stat_ref == gen_ref: # Update Statistics where Ref/Alt non switched
                                                li_pos.append(MAF(li_pos))
                                                li_pos.append(MAC(li_pos))
						li_pos.append(EAC(li_pos))
                                                li_pos.append((str(float(li_pos[AF]))))
                                                li_pos[BETA] = str(float(li_pos[BETA])) #BETA->OR
                                                count_m = count_m + 1
                                                li_pos.append("\n")
                                                OUT.write("\t".join(li_pos))
                                        else:
                                                continue
                                elif chr_n.isdigit() and int(chr_n) > 23: # for non autosomal & sex chromosomes 
                                        continue
                                elif (chr_n.isdigit() and int(chr_n) < 23 ) and  monomorphic_filter(li_pos) is False: # This is the body of the computational part all autosomes
                                        gen_ref = genome.fetch(chr_n,int(bp_pos)-1,int(bp_pos)) # Query reg genome
                                        if stat_ref != gen_ref:
                                                count_mm = count_mm + 1
                                                li_pos[2] = gen_ref # swap references
                                                li_pos[3] = stat_ref # swap alternatives
                                                li_pos[BETA] = str(float(li_pos[BETA]) * -1) # BETA 
                                                li_pos.append(MAF(li_pos))
						li_pos.append(MAC(li_pos))
                                                li_pos[N_alt], li_pos[N_ref] = li_pos[N_ref], li_pos[N_alt]
						li_pos.append(EAC(li_pos))
                                                li_pos.append(str(1 - float(li_pos[AF])))
                                                li_pos.append("\n")
                                                OUT.write("\t".join(li_pos))
                                        elif stat_ref == gen_ref:
                                                li_pos.append(MAF(li_pos))
                                                li_pos.append(MAC(li_pos))
						li_pos.append(EAC(li_pos))
                                                li_pos.append((str(float(li_pos[AF]))))
                                                li_pos[BETA] = str(float(li_pos[BETA])) #BETA->OR
                                                count_m = count_m + 1
                                                li_pos.append("\n")
                                                OUT.write("\t".join(li_pos))
                                        else:
                                                continue
                                else:
                                        continue
                	        count = count + 1
		OUT.close()
		return str(count_mm) + " Reference mismatches: Reference allele is effect allele" + "\n" + str(count_m) + " Matches to reference genome" + "\n" + str(count) + " Sites checked"
            

