import utils
from utils import File_Reader as FR
from utils import Task_Follower as TF
import random

strippattern = "^\"|\"$"
pubmed_file = FR("../PUBMED_DATA/pubmed_data_2606.txt", sep = "\t", suppress_newlines = True, skiplines = 1, encoding = "CP1252", strip_chars_pattern = strippattern)

drugs_file = FR("../DRUG_LISTS/full_drug_list.txt", sep = ";", suppress_newlines = True, encoding = "utf-16")

pubmed = pubmed_file.readlines()
drugs = drugs_file.readlines()


match = {}

for article in pubmed:
	match[int(article[1])] = ("","",[],"")


print(len(match))


# tf = TF(len(drugs))

for names in drugs:
	for article in pubmed:
		found = False
		title = article[5]
		description = article[6]
		pmid = int(article[1])
		year = article[3]
		for n in names:
			if (n in title or n in description) and n!="na" and n!="NA":
				found = True
		if found:
			match[pmid] = (year, title, match[pmid][2]+names, description)
		
	# tf.step()

print(match[28980060])

i= 0
for k,v in match.items():
	if v==("","",[],""):
		i+=1

print(i)

# with open("../PUBMED_DATA/pubmedNdrugs_2.txt", "w", encoding = "utf-8") as fp:
# 	for k,v in match.items():
# 		if v[2]:
# 			fp.write("\t".join([str(k),v[0], v[1],v[2][0]])+"\n")
# 		else:
# 			fp.write("\t".join([str(k),v[0], v[1],""])+"\n")



# with open("../pubmed_data_2606_noDRUG_2.txt", "w", encoding = "utf-8") as fp:
# 	for k,v in match.items():
# 		if v == []:
# 			fp.write(str(k)+"\n")


pop = list(range(0,2605))
samp = random.sample(pop, 40)
with open("../PUBMED_DATA/positiveControl_3.txt", "w", encoding = "utf-8") as fp:

	a = []
	i=0
	for m in match.keys():
		if i in samp:
			a.append(m)
		i+=1

	for k in a:
		fp.write("\t".join([str(k), match[k][1], match[k][3], ";".join(match[k][2]) ])+"\n")
