import os

if __name__ == "__main__":
	filenames=os.listdir("units")
	filenamesnum=len(filenames)
	i = 0
	while i <= filenamesnum:
		i += 1
		if i == filenamesnum or filenames[i] == None:
			print("i is None")
			break
		else:
			k = open(("units/"+filenames[i]), "r", encoding="utf-8").read()
			p = k.split("\n")[0].split("|")[0]
			if p == None or p == "":
				p = "None"
			whhe = (int(filenames[i].strip("Unit_Explanation_ko.csv")) - 1)
			open("catdb.csv", "a+", encoding="utf-8").write((p+","+str(whhe)+"\n"))

	print("finished")
	#Unit_Explanation11_ko.csv