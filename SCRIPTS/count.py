"""

Count drug occurences from input file. Format of said file should be checked.
"""

from utils import File_Reader as FR

file = FR("../PUBMED_DATA/pubmedNdrugs.latest.txt", sep = '\t', suppress_newlines = True, skiplines = 0, encoding = "utf-8")

counter = {}

for line in file.iter():
	drug = line[3]
	drug = drug.split(";")[0]
	if drug:
		if drug not in counter:
			counter[drug] = 1
		else:
			counter[drug]+=1




print(counter)

print(len(counter))

s = sorted(counter.items(), key=lambda x: x[1])[::-1]

print(s)

with open("../PUBMED_DATA/drug_counter.latest.txt", 'w', encoding = "utf8") as fp:
	for i in s:
		fp.write(("\t".join([i[0],str(i[1])])+'\n'))