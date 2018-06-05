from utils import File_Reader as FR



charstrip = "^|^\"| $|\"$"
nosym_file = FR("../DRUG_LISTS/tbl_Abst_drug_LIST_noSYMBOLS 2018 05 17.txt", sep = "\t", suppress_newlines = True, skiplines = 1, strip_chars_pattern = charstrip, encoding = "utf-16")
supp_file  = FR("../DRUG_LISTS/tbl_Abst_drug_LIST_SUPP 2018 05 31.txt", sep = "\t", suppress_newlines = True, skiplines = 1, strip_chars_pattern = charstrip, encoding = "utf-16")
dlist_file = FR("../DRUG_LISTS/tbl_Abst_drug_vs_symbols_match - DRUG_LIST 2018 05 17.txt", sep = "\t", suppress_newlines = True, skiplines = 1, strip_chars_pattern = charstrip, encoding = "utf-16")
dmatch_file= FR("../DRUG_LISTS/tbl_Abst_drug_vs_symbols_match - DRUG_MATCH 2018 05 27.txt", sep = "\t", suppress_newlines = True, skiplines = 1, strip_chars_pattern = charstrip, encoding = "utf-16")



nosym = nosym_file.readlines()
supp = supp_file.readlines()
dlist = dlist_file.readlines()
dmatch = dmatch_file.readlines()


for f in [supp, nosym, dlist, dmatch]:
	for s in f:
		while "" in s:
			s.remove("")

final_ref = []
pool = []

for f in [supp, nosym, dlist, dmatch]:

	for item in f:
		for name in item:
			if name.lower() not in item:
				item.append(name.lower()) 
			if name.upper() not in item:
				item.append(name.upper())
			if name[0].upper()+name[1:] not in item:
				item.append(name[0].upper()+name[1:])
			if not name:
				item.pop(item.index(name))

		pool.append(item)


while pool:
	elems = pool.pop()
	res = []
	while elems:
		searching = elems.pop()
		if searching not in res:
			res.append(searching)
			for p in pool:
				if searching in p:
					for i in p:
						elems.append(i)
					pool.pop(pool.index(p))

	final_ref.append(sorted(res))


csv = []
for i in final_ref:
	csv.append(";".join(i))

with open("../DRUG_LISTS/full_drug_list.txt",'w', encoding = "utf-16") as fp:
	for drug in csv:
		fp.write(drug+"\n")