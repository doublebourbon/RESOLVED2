"""
Needs work
"""

import utils
from utils import File_Reader as FR
from utils import Task_Follower as TF
import random
import re
from string import punctuation

strippattern = "^\"|\"$"
pubmed_file = FR("../PUBMED_DATA/pubmed_data_2606.txt", sep = "\t", suppress_newlines = True, skiplines = 1, encoding = "CP1252", strip_chars_pattern = strippattern)

drugs_file = FR("../DRUG_LISTS/full_drug_list.latest.txt", sep = ";", suppress_newlines = True, encoding = "utf-8")

pubmed = pubmed_file.readlines()
drugs = drugs_file.readlines()


match = {}

for article in pubmed:
	match[int(article[1])] = ("","",[],"")


print(len(drugs))


tf = TF(len(drugs))

for names in drugs:
	tf.step()
	for article in pubmed:
		found = False
		title = article[5]
		description = article[6]
		pmid = int(article[1])
		year = article[3]
		for n in names:
			pat = n
			if "[" in pat:
				pat = pat.replace("[", "\\[")
			if "]" in pat:
				pat = pat.replace("]", "\\]")
			if "(" in pat:
				pat = pat.replace("(", "\\(")
			if ")" in pat:
				pat = pat.replace(")", "\\)")
			# re_pattern = "(^"+pat+"["+punctuation+"])|(["+punctuation+"]"+pat+"["+punctuation+"])|( "+pat+"$)"
			re_pattern = r'\b'+pat
			# if (n in title or n in description) and n!="na" and n!="NA":
			if re.search(re_pattern, title) or re.search(re_pattern, description):
				found = True
		if found:
			match[pmid] = (year, title, match[pmid][2]+names, description)
		
	# tf.step()

print(match[28980060])

missing= 0
for k,v in match.items():
	if v==("","",[],""):
		missing+=1

print(missing)

# with open("../PUBMED_DATA/pubmedNdrugs.latest.txt", "w", encoding = "utf-8") as fp:
# 	for k,v in match.items():
# 		if v[2]:
# 			fp.write("\t".join([str(k),v[0], v[1],v[2][0]])+"\n")
# 		else:
# 			fp.write("\t".join([str(k),v[0], v[1],""])+"\n")


#### Missing
with open("../PUBMED_DATA/pubmed_data_2606_noDRUG_4.txt", "w", encoding = "utf-8") as fp:
	for k,v in match.items():
		if v == ("","",[],""):
			fp.write(str(k)+"\n")



# #### Positive control generator


# pop = list(range(0,2606-missing))
# samp1 = random.sample(pop, 40)
# samp2 = random.sample(pop, 40)
# samp3 = random.sample(pop, 40)

# no_miss = match.copy()
# del_keys = []
# for k,v in no_miss.items():
# 	if v==("","",[],""):
# 		del_keys.append(k)

# for k in del_keys:
# 	del no_miss[k]


# with open("../PUBMED_DATA/positiveControl_1.txt", "w", encoding = "utf-8") as fp:

# 	a = []
# 	i=0
# 	for m in no_miss.keys():
# 		if i in samp1:
# 			a.append(m)
# 		i+=1

# 	for k in a:
# 		fp.write("\t".join([str(k), no_miss[k][1], no_miss[k][3], ";".join(no_miss[k][2]) ])+"\n")


# with open("../PUBMED_DATA/positiveControl_2.txt", "w", encoding = "utf-8") as fp:

# 	a = []
# 	i=0
# 	for m in no_miss.keys():
# 		if i in samp2:
# 			a.append(m)
# 		i+=1

# 	for k in a:
# 		fp.write("\t".join([str(k), no_miss[k][1], no_miss[k][3], ";".join(no_miss[k][2]) ])+"\n")


# with open("../PUBMED_DATA/positiveControl_3.txt", "w", encoding = "utf-8") as fp:

# 	a = []
# 	i=0
# 	for m in no_miss.keys():
# 		if i in samp3:
# 			a.append(m)
# 		i+=1

# 	for k in a:
# 		fp.write("\t".join([str(k), no_miss[k][1], no_miss[k][3], ";".join(no_miss[k][2]) ])+"\n")
