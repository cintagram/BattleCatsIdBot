import os

if __name__ == "__main__":
	filenames=os.listdir("resLocal")
	filenamesnum=len(filenames)
	i = 0
	while i <= filenamesnum:
		i += 1
		if i == filenamesnum or filenames[i] == None:
			print("i is None")
			break
		else:
			if not "Unit_Explanation" in filenames[i]:
				os.remove("resLocal/"+filenames[i])
			else:
				pass
	
			

	filenames=os.listdir("resLocal")
	filenamesnum=len(filenames)
	i = 0
	while i <= filenamesnum:
		i += 1
		if i == filenamesnum or filenames[i] == None:
			print("i is None")
			break
		else:
			k = open(("resLocal/"+filenames[i]), "r", encoding="utf-8").read()
			p = k.split("\n")[0].split("|")[0]
			if p == None or p == "":
				p = "None"
			whhe = (int(filenames[i].strip("Unit_Explanation_.csv").strip("en").strip("ko").strip("tw").strip("ja")) - 1)
			open("catdb.csv", "a+", encoding="utf-8").write((p+","+str(whhe)+"\n"))

	print("finished")
	#Unit_Explanation11_ko.csv
