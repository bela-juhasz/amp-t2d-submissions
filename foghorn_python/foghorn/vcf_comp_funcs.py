import sys

def GT_comp(GT, lines_holder, sample_index, mis, fields):
    if GT in {"0|1", "1|0", "1/0", "0/1"}:
        lines_holder.append("".join([str(sample_index), ":", "1"]))
        sample_index = sample_index + 1
        return sample_index, lines_holder
    elif GT in {"1|1", "1/1"}:
        lines_holder.append("".join([str(sample_index), ":", "2"]))
        sample_index = sample_index + 1
        return sample_index, lines_holder
    elif GT in {".|1", "1|.", "./1", "1/.", ".|0", "0|.", "./0", "0/."}:  # missing variants, Key value with variants and sample is better than this. test dataset has little missing variants so not an issue just yet
        string = "".join(["Sample# ", str(sample_index), " has a single allele missing at pos ->  ", str(fields[:4]), "\n"])
        mis.append(string)
        sample_index = sample_index + 1
        return sample_index, mis
    elif GT in {"./.", ".|."}:
        string = "".join(["Sample# ", str(sample_index), " has a both alleles missing at pos ->  ", str(fields[:4]), "\n"])
        mis.append(string)
        sample_index = sample_index + 1
        return sample_index, mis
    else:
        sample_index = sample_index + 1
        return sample_index

def DS_comp(DS, lines_holder, sample_index):
    if float(DS) != 0:
        string = "".join([str(sample_index), ":", str(DS)])
        lines_holder.append(string)
        sample_index = sample_index + 1
        return lines_holder, sample_index
    else:
        sample_index = sample_index + 1
        return sample_index

def mult_al(GT, lines_holderMS, sample_indexMS, mis, fields):
    if GT in {"2|2", "2/2"}:
        string = "".join([str(sample_indexMS), ":", "2"])
        lines_holderMS.append(string)
        return sample_indexMS, lines_holderMS
    elif GT in {"0|2", "2|0", "2/0", "0/2"}:  # need to clarify the odds of seeing 1|2. This will most probably be a sequencing error. So for the moment I am only including the referernce "0"
        # This is one implementation the second is to just add extra indices
        string = "".join([str(sample_indexMS), ":", "1"])
        lines_holderMS.append(string)
        return sample_indexMS, lines_holderMS
    elif GT in {".|.", "./."}:
        string = "".join(["Sample# ", str(sample_indexMS), " has a both alleles missing at pos ->  ", str(fields[:5]), "\n"])
        mis.append(string)
        sample_indexMS = sample_indexMS + 1
        return sample_indexMS, mis
    elif GT in {".|2", "2|.", "2/.", "./2", ".|1", "1|.", "1/.", "./1", ".|0", "0|.", "0/.", "./0"}:
        string = "".join(["Sample# ", str(sample_indexMS), " has asingle allele missing at pos ->  ", str(fields[:5]), "\n"])
        mis.append(string)
        sample_indexMS = sample_indexMS + 1
        return sample_indexMS, mis
    else:
        return None

def GT(line, out, mis_vars):
    if not line.startswith("##") and not line.startswith("#"):  # Need to spend time making robust and reporting file format and missingness errors
        fields = line.strip().split()
        if "GT" not in fields[8]:
            sys.exit("No genotype tag in format field")  # raise error that there is no GT fields in
        sample_index = sample_indexMS = 0
        lines_holderMS = []  # refresh every iteration need to check if this has any effect on the memory management of large datasets
        lines_holder = []
        mis = []
        lines_holder.extend(fields[:4])  # append first few columns
        if "," in fields[4]:
            lines_holderMS.extend(fields[:4])
            lines_holder.append(str(str(fields[4]).split(",")[0]))  # ALT1
            lines_holderMS.append(str(str(fields[4]).split(",")[1]))  # ALT2
            for column in fields[9:]:
                GT = column.strip().split(":")[0]
                GT_comp(GT, lines_holder, sample_index, mis, fields)
                sample_index = sample_index + 1
                mult_al(GT, lines_holderMS, sample_indexMS, mis, fields)
                sample_indexMS = sample_indexMS + 1
        else:
            lines_holder.append(fields[4])
            for column in fields[9:]:
                GT = column.strip().split(":")[0]
                GT_comp(GT, lines_holder, sample_index, mis, fields)
                sample_index = sample_index + 1
        lines_holder.append("")
        lines_holderMS.append("")
        mis.append("")
        out.write('\t'.join(map(str, lines_holder)))
        out.write("\n")
        mis_vars.write('\t'.join(map(str, mis)))
        if len(lines_holderMS) > 1:  # the "" appendage makes the list non-empty need to convert to hexdecimal again to compare to foghorn
            out.write('\t'.join(map(str, lines_holderMS)))
            mis_vars.write('\t'.join(map(str, mis)))
            out.write('\n')
    elif not line.startswith("##") and line.startswith("#"):
        field = line.strip().split()
        out.write("#CHR" + '\t' + "POS" + '\t' + "ID" + '\t' + "Ref" + '\t' + "ALT" + '\t' + '\t'.join(map(str, field[9:])))
        out.write('\n')

def DS(line, out):
    if not line.startswith("##") and not line.startswith("#"):
        fields = line.strip().split()
        if "DS" not in fields[8]:
            sys.exit("No dosage (DS/DOS) found in format field")  # raise error that there is no GT fields in VCF
        else:
            DOSidx = fields[8].split(":").index("DS")
        sample_index = 0
        lines_holder = []
        lines_holder.extend(fields[:4]) # append first few columns
        if "," in fields[4]:  # not set up for multiple variants yet this is redundant until multivariants are incorported
            lines_holder.append(str(str(fields[4]).split(",")[0]))  # ALT1
            for column in fields[9:]:
                DS = column.strip().split(":")[int(DOSidx)]
                DS_comp(DS, lines_holder, sample_index)
                sample_index = sample_index + 1
        else:
            lines_holder.append(fields[4])
            for column in fields[9:]:
                DS = column.strip().split(":")[int(DOSidx)]
                DS_comp(DS, lines_holder, sample_index)
                sample_index = sample_index + 1
        lines_holder.append("")
        out.write('\t'.join(map(str, lines_holder)))
        out.write("\n")
    elif not line.startswith("##") and line.startswith("#"):
        field = line.strip().split()
        out.write("#CHR" + '\t' + "POS" + '\t' + "ID" + '\t' + "Ref" + '\t' + "ALT" + '\t' + '\t'.join(map(str, field[9:])))
        out.write('\n')

def compress_genotypes(input, output, missing_output):
    for line in input:
        GT(line, output, missing_output)

def compress_dosages(input, output):
    for line in input:
        DS(line, output)
