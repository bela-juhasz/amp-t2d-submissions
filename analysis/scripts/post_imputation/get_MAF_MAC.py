import sys

param = sys.argv


with open("MAF_MAC_from_query.txt","w") as OUT:
	string="VAR_ID" + "\t" + "MAF" + "\t" + "AN" + "\t"+ "MAC" + "\n"
	OUT.write(string)
	for line in sys.stdin:
		line = line.strip()
		parts = line.split("\t")
		fields = parts
		var_id = fields[0] + "_" + fields[1] + "_" + fields[2] + "_" + fields[3]
		AF = fields[5]
		MAF = fields[4]
		AN = fields[6]
		AC = fields[7]
		if float(AC) <= (float(AN)/2):
			out = var_id + "\t" + MAF + "\t" + AN + "\t"+ AC + "\n"
			OUT.write(out)
		elif float(AC) > (float(AN)/2):
			MAC = int(AN) - int(AC)
			out = var_id + "\t" + MAF + "\t" + AN + "\t" + str(MAC) +"\n"
			OUT.write(out)