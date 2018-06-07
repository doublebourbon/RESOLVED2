import sys
import re
import os

class File_Reader():
	"""Classe de lecture de fichiers text simples (txt, csv, tsv...).
	
	:param file_name: chemin du fichier à lire
	:param sep: séparateur de champ, aucun par defaut. En cas de separateur, chaque ligne sera une liste python avec un element pour chaque champ
	:param suppress_newlines: si on veut enlever les \n à la fin de chaque ligne, vrai par defaut
	:param skiplines: nombre de lignes à ignorer en début de fichier, 0 par defaut
	:param strip_chars_pattern: expression reguliere pour enlever certains caracteres ou expressions (ex: expace en debut de ligne), auncune par defaut
	:param encoding: l'encodage du fichier, par defaut utf8

	:example:

	#Initialiser avec le chemin du fichier et les parametres voulus
	my_file = File_Reader("chemin/vers/lefichier/")
	#lecture ligne par ligne
	for line in my_file.iter():
		do_something(line)
	#OU recuperation de chaque ligne dans une liste
	all_lines = my_file.readlines()
	#Une fois le fichier parcouru, il faut reutiliser cette classe si l'on veut relire le fichier.
	"""
	def __init__(self, file_name, sep = "", suppress_newlines = True, skiplines = 0, strip_chars_pattern = "", encoding = ""):
		self.file_name = file_name
		self.sep = sep
		self.suppress_newlines = suppress_newlines
		self.skiplines = skiplines
		self.strip_chars_pattern = strip_chars_pattern
		self.encoding = "utf-8"
		if encoding:
			self.encoding = encoding

	def char_strip(self,string, pattern):
		return re.sub(pattern, '', string)

	def iter(self):
		
		self.fp = open(self.file_name, encoding = self.encoding)
		self.line = self.fp.readline()

		for i in range(self.skiplines):
			self.line = self.fp.readline()

		while self.line:
			
			if self.suppress_newlines:
				self.line = self.line[:-1]

			if self.sep:
				self.line = self.line.split(self.sep)
				if self.strip_chars_pattern:
					for i in range(len(self.line)):
						self.line[i] = self.char_strip(self.line[i], self.strip_chars_pattern)
			
			if self.strip_chars_pattern and type(self.line)!=list:
				self.line = self.char_strip(self.line, self.strip_chars_pattern)

			yield self.line
			self.line = self.fp.readline()

		self.fp.close()

	def readlines(self):
		text = []
		for self.line in self.iter():
			text.append(self.line)
		return(text)


class Task_Follower():
	"""Mini barre de progression en pourcentage pour les executions linéaire longues.

	#initialiser avec le nombre d'opérations
	t = Task_Follower(count)
	#incrémenter l'avencement
	t.step()"""
	def __init__(self, taskcount, message = "Completion: "):
		self.taskcount = taskcount
		self.done = 0
		self.message = message
		self.gen = self.ini()

	def ini(self):
		return self.next()

	def step(self):
		sys.stdout.write(next(self.gen))
		sys.stdout.flush()

	def next(self):
		while self.done < self.taskcount+1:
			yield str(self.message + "%.2f \r" % (100*self.done/self.taskcount))
			self.done+=1
		while True:
			yield "Task Done\r"


def head(l, start = 0, stop = 5):
	"""Equivalent de l'outil linux head."""
	print(l[start:stop])


class File_Maker():
	def __init__(self, path, replace_old = False, olddata_dir = "", version_control = True, encoding = "utf-8", mode = "w", latest_string = "latest"):
		
		self.path = path
		self.file_name = self.get_filename()
		self.extension = self.get_extension()
		self.save_dir = self.get_savedir()
		self.olddata_dir = olddata_dir

		self.replace_old = replace_old
		self.version_control = version_control

		self.mode = mode
		self.encoding = encoding

		
		self.fp = None

		self.original_dir = os.getcwd()


	# def setcwd(self, dir):
	# 	os.chdir(dir)

	def get_filename(self):
		name = (self.path.split("/")[-1])
		if '.' in name:
			name = ".".join(name.split('.')[0:-1])
		return name

	def get_extension(self):
		ext = self.path
		if ".." in ext:
			ext = self.path.split("..")[-1]

		if '.' in ext:
			ext = ext.split(".")[-1]
			return "."+ext
		return ""

	def get_savedir(self):
		sd = "/".join(self.path.split("/")[0:-1])
		return sd


	def get_filepointer(self):
		# self.setcwd(self.original_dir)
		# self.setcwd(self.save_dir)
		if self.replace_old and not self.version_control:
			self.fp = open(self.file_name+self.extension, self.mode, encoding = self.encoding)
			return self.fp

		if not self.replace_old and self.version_control:
			self.fp = open(self.file_name, self.mode, encoding = self.encoding)
			return self.fp



	def close(self):
		if self.fp:
			self.fp.close