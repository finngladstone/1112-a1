import os, sys, stat

from datetime import datetime

import grp, pwd

# fn definitions 

def groupread(status):
	return bool(status.st_mode & stat.S_IRGRP)

def groupexec(status):
	return bool(status.st_mode & stat.S_IXGRP)

# https://www.delftstack.com/howto/python/python-find-file/#find-file-with-the-os.walk-function-in-python

def rectify_path(name, start):
	for root, dirname, filename in os.walk(start):
		if name in filename:
			return os.path.join(root, name)

def gather_and_write(foutput, path):

	path_temp = path.strip("\n")

	if not os.path.exists(os.path.abspath(path_temp)):
		path_temp = rectify_path(path.strip("\n"), os.getcwd())

	if path_temp == None:
		raise FileNotFoundError

	status = os.stat(path_temp)

	# make format corrections on time variable s
	moddate = datetime.fromtimestamp(status.st_mtime).strftime("%b %d  %Y")
	accdate = datetime.fromtimestamp(status.st_atime).strftime("%b %d  %Y")

	usr = pwd.getpwuid(status.st_uid)
	gp = grp.getgrgid(status.st_gid)

	foutput.write(path.strip("\n") + " Group Readable: " + str(groupread(status)) + ", Group Executable: " + str(groupexec(status)) + " ")
	foutput.write("Size: {a}, Owner: {b}, Group: {c}, last modified date: {d}, last access date: {e}\n".format(
		a = status.st_size,
		b = usr[0],
		c = gp[0],
		d = moddate,
		e = accdate)
	)

	current = stat.S_IMODE(os.lstat(path_temp).st_mode)

	if groupexec(status):
		# change to read/write
		os.chmod(path_temp, current & ~stat.S_IXGRP)
	else:
		# change to read/write/execute
		os.chmod(path_temp, current | stat.S_IXGRP)

	return None


def main():

	foutput = open("output.txt", "w") # creates or opens with overwrite the output file

	# list for files that need to be manipulated
	File_ls = []

	if os.path.exists('filelist.txt'):
		with open('filelist.txt') as f:

			for lines in f:
				File_ls.append(lines)

	else:
		foutput.write("filelist.txt can not be found\n")
		foutput.close()
		sys.exit(0)

	for path in File_ls:
		try: 
			gather_and_write(foutput, path)

		except FileNotFoundError:
			foutput.write("{} can not be found\n".format(path.strip("\n")))
				
	foutput.close()
	assert foutput.closed


if __name__ == '__main__':
	main()
