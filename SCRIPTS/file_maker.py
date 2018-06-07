from utils import File_Maker as FM

file = FM("GRAPH/test78324264.txt", replace_old = True, version_control = False)

print(file.get_filename())
print(file.get_extension())
print(file.get_savedir())
print(file.original_dir)




fp = file.get_filepointer()



fp.write("adzaf")
fp.write("sth")
fp.write("rthter")
fp.write("rthet")

fp.close()