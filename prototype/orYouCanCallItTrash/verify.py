import os
textt = input("are you sure?")
textt2 = input("are you sure?")
textt = input("are you sure?")
textt2 = input("are you sure?")
textt = input("are you sure?")

dirtxt = "ddata/txt"
diralign = "mid_data/aligned"
image = []

for i, filename in enumerate(os.listdir(diralign)):
	image.append(filename[8:len(filename)-8]+".txt")

for i, filename in enumerate(os.listdir(dirtxt)):
	if filename not in image:
		os.rename(dirtxt+"/"+filename, "ddata/textQuarantined/"+filename)