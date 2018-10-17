import sys

param = sys.argv


with open("MAC_MAF.txt","w") as OUT:
	string="VAR_ID" + "\t" + "MAF" + "\t" + "AN" + "\t"+ "MAC" + "\n"
	OUT.write(string)
	for line in sys.stdin:
		if not line.startswith("#"):
			fields = line.strip().split()
			var_id = fields[0] + "_" + fields[1] + "_" + fields[3] + "_" + fields[4]
			INFO= fields[5].strip().split(";")
			for i in range(len(INFO)):
				if INFO[i].split("=")[0] =="AC":
					AC = INFO[i].split("=")[1]
				elif INFO[i].split("=")[0] =="AN":
					AN = INFO[i].split("=")[1]
				elif INFO[i].split("=")[0] =="MAF":
					MAF = INFO[i].split("=")[1]
			if int(AC) < (float(AN)/2):
				out = var_id + "\t" + MAF + "\t" + AN + "\t"+ AC + "\n"
				OUT.write(out)
			elif int(AC) > (float(AN)/2):
				MAC = int(AN) - int(AC)
				out = var_id + "\t" + MAF + "\t" + AN + "\t"
				outl = out + str(MAC) + "\n"
				OUT.write(outl)
