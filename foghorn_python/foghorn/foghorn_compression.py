"""
Functions that implement foghorn VCF compression algorithms
"""
# pylint: disable=C0103

import sys

def compress_genotype(genotype, lines_holder, sample_index, mis, fields):
    """
    Transform a genotype into another format (sample_index:num_of_alt_alleles)

    :param genotype: genotype value for the sample at that position
    :type genotype: basestring
    :param lines_holder: container to store transformed information in new format
    :type lines_holder: list
    :param sample_index: the index of sample in the sample list
    :type sample_index: int
    :param mis: container to store missing allelic information
    :type mis: list
    :param fields: the split list of a VCF line
    :type fields: list
    """
    if genotype in {"0|1", "1|0", "1/0", "0/1"}:
        lines_holder.append(str(sample_index) + ":1")
    elif genotype in {"1|1", "1/1"}:
        lines_holder.append(str(sample_index) + ":2")
    elif genotype in {".|1", "1|.", "./1", "1/.", ".|0", "0|.", "./0", "0/."}:  # missing variants, Key value with variants and sample is better than this. test dataset has little missing variants so not an issue just yet
        string = "".join(["Sample# ", str(sample_index), " has a single allele missing at pos ->  ", str(fields[:4]), "\n"])
        mis.append(string)
    elif genotype in {"./.", ".|."}:
        string = "".join(["Sample# ", str(sample_index), " has a both alleles missing at pos ->  ", str(fields[:4]), "\n"])
        mis.append(string)

def compress_dosage(dosage, lines_holder, sample_index):
    """
    Transform a dosage information into another format (sample_index:dosage)

    :param dosage: the dosage information stored in original VCF
    :type dosage: basestring
    :param lines_holder: container to store transformed information in new format
    :type lines_holder: list
    :param sample_index: the index of sample in the sample list
    :type sample_index: int
    """
    if dosage != "0":
        string = str(sample_index) + ":" + dosage
        lines_holder.append(string)

def compress_genotype_multiallelic(genotype, lines_holderMS, sample_indexMS, mis, fields):
    """
    Transform a genotype into another format (sample_index:num_of_alt_alleles) for
    multi-allelic sites

    :param genotype: genotype value for the sample at that position
    :type genotype: basestring
    :param lines_holderMS: container to store transformed information in new format
    :type lines_holderMS: list
    :param sample_indexMS: the index of sample in the sample list
    :type sample_indexMS: int
    :param mis: container to store missing allelic information
    :type mis: list
    :param fields: the split list of a VCF line
    :type fields: list
    """
    if genotype in {"2|2", "2/2"}:
        lines_holderMS.append(str(sample_indexMS) + ":2")
    elif genotype in {"0|2", "2|0", "2/0", "0/2"}:  # need to clarify the odds of seeing 1|2. This will most probably be a sequencing error. So for the moment I am only including the referernce "0"
        # This is one implementation the second is to just add extra indices
        lines_holderMS.append(str(sample_indexMS) + ":1")
    elif genotype in {".|.", "./."}:
        string = "".join(["Sample# ", str(sample_indexMS), " has a both alleles missing at pos ->  ", str(fields[:5]), "\n"])
        mis.append(string)
    elif genotype in {".|2", "2|.", "2/.", "./2", ".|1", "1|.", "1/.", "./1", ".|0", "0|.", "0/.", "./0"}:
        string = "".join(["Sample# ", str(sample_indexMS), " has a single allele missing at pos ->  ", str(fields[:5]), "\n"])
        mis.append(string)

def transform_genotypes(line, out, mis_vars):
    """
    Process a VCF line for genotypes and transform them into the new format

    :param line: a line in a VCF (including headers)
    :type line: basestring
    :param out: file to write transformed information into
    :type out: file
    :param mis_vars: file to write missing allelic information into
    :type mis_vars: file
    """
    if not line.startswith("##") and not line.startswith("#"):  # Need to spend time making robust and reporting file format and missingness errors
        fields = line.strip().split()
        if "GT" not in fields[8]:
            sys.exit("No genotype tag in format field")  # raise error that there is no GT fields in
        else:
            GTidx = fields[8].split(":").index("GT")
        sample_index = sample_indexMS = 0
        lines_holderMS = []  # refresh every iteration need to check if this has any effect on the memory management of large datasets
        lines_holder = []
        mis = []
        lines_holder.extend(fields[:2])  # append first few columns
        lines_holder.extend(fields[3])
        if "," in fields[4]:
            lines_holderMS.extend(fields[:2])  # append first few columns
            lines_holderMS.extend(fields[3])
            lines_holder.append(fields[4].split(",")[0])  # ALT1
            lines_holderMS.append(fields[4].split(",")[1])  # ALT2
            for column in fields[9:]:
                GT = column.strip().split(":")[GTidx]
                compress_genotype(GT, lines_holder, sample_index, mis, fields)
                sample_index = sample_index + 1
                compress_genotype_multiallelic(GT, lines_holderMS, sample_indexMS, mis, fields)
                sample_indexMS = sample_indexMS + 1
        else:
            lines_holder.append(fields[4])
            for column in fields[9:]:
                GT = column.strip().split(":")[GTidx]
                compress_genotype(GT, lines_holder, sample_index, mis, fields)
                sample_index = sample_index + 1
        lines_holder.append("")
        lines_holderMS.append("")
        mis.append("")
        out.write('\t'.join(lines_holder))
        out.write("\n")
        mis_vars.write('\t'.join(mis))
        if len(lines_holderMS) > 1:  # the "" appendage makes the list non-empty need to convert to hexdecimal again to compare to foghorn
            out.write('\t'.join(lines_holderMS))
            out.write('\n')
    elif not line.startswith("##") and line.startswith("#"):
        field = line.strip().split()
        out.write("#CHR" + '\t' + "POS" + '\t' + "REF" + '\t' + "ALT" + '\t' + '\t'.join(field[9:]))
        out.write('\n')

def transform_dosages(line, out):
    """
    Process a VCF line for dosages  and transform them into the new format

    :param line: a line in a VCF (including headers)
    :type line: basestring
    :param out: file to write transformed information into
    :type out: file
    """
    if not line.startswith("##") and not line.startswith("#"):
        fields = line.strip().split()
        if "DS" not in fields[8]:
            sys.exit("No dosage (DS/DOS) found in format field")  # raise error that there is no DS fields in VCF
        else:
            DOSidx = fields[8].split(":").index("DS")
        sample_index = 0
        lines_holder = []
        lines_holder.extend(fields[:2])
        lines_holder.extend(fields[3])
        if "," in fields[4]:  # not set up for multiple variants yet this is redundant until multivariants are incorported
            lines_holder.append(str(fields[4]).split(",")[0])  # ALT1
            for column in fields[9:]:
                DS = column.strip().split(":")[DOSidx]
                compress_dosage(DS, lines_holder, sample_index)
                sample_index = sample_index + 1
        else:
            lines_holder.append(fields[4])
            for column in fields[9:]:
                DS = column.strip().split(":")[DOSidx]
                compress_dosage(DS, lines_holder, sample_index)
                sample_index = sample_index + 1
        lines_holder.append("")
        out.write('\t'.join(lines_holder))
        out.write("\n")
    elif not line.startswith("##") and line.startswith("#"):
        field = line.strip().split()
        out.write("#CHR" + '\t' + "POS" + '\t' + "REF" + '\t' + "ALT" + '\t' + '\t'.join(field[9:]))
        out.write('\n')

def compress_genotypes(vcf, output, missing_output):
    """
    Entry function to take a VCF input and write the transformed genotype information to new output

    :param vcf: file for reading lines from VCF
    :type vcf: file
    :param output: file to write transformed genotype information into
    :type output: file
    :param missing_output: file to write missing allelic information into
    :type missing_output: file
    """
    for line in vcf:
        transform_genotypes(line, output, missing_output)

def compress_dosages(vcf, output):
    """
    Entry function to take a VCF input and write the transformed dosage information to new output

    :param vcf: file for reading lines from VCF
    :type vcf: file
    :param output: file to write transformed dosage information into
    :type output: file
    """
    for line in vcf:
        transform_dosages(line, output)
