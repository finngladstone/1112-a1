import os, sys, stat

from plistlib import InvalidFileException

from datetime import datetime

import grp, pwd

# boolean fns for checking read/exec perms. used in output and for flipping exec 

def groupread(status):
	return bool(status.st_mode & stat.S_IRGRP)

def groupexec(status):
	return bool(status.st_mode & stat.S_IXGRP)

# https://www.delftstack.com/howto/python/python-find-file/#find-file-with-the-os.walk-function-in-python

# pathfinding function for creating a path if none is specified. i thought this was for the hidden test case so might be unnecessary

def rectify_path(name, start):
	for root, dirname, filename in os.walk(start):
		if name in filename:
			return os.path.join(root, name)

# takes the output file and path to the file in question and writes its data + flips exec perms 

def gather_and_write(foutput, path):

	path_temp = path.strip("\n")
	
	if os.path.isdir(path_temp):
		raise InvalidFileException 

	if not os.path.exists(os.path.abspath(path_temp)): # will rectify path if it is broken 
		path_temp = rectify_path(path.strip("\n"), os.getcwd())
	
	if path_temp == None: # executed if file is unreachable
		raise FileNotFoundError

	status = os.stat(path_temp)

	# make format corrections on time variable s
	moddate = datetime.fromtimestamp(status.st_mtime).strftime("%b %d  %Y")
	accdate = datetime.fromtimestamp(status.st_atime).strftime("%b %d  %Y")

	usr = pwd.getpwuid(status.st_uid) # obtain user and group names using pwd and grp modules
	gp = grp.getgrgid(status.st_gid)

	foutput.write(path.strip("\n") + " Group Readable: " + str(groupread(status)) + ", Group Executable: " + str(groupexec(status)) + " ")
	foutput.write("Size: {a}, Owner: {b}, Group: {c}, last modified date: {d}, last access date: {e}\n".format(
		a = status.st_size,
		b = usr[0],
		c = gp[0],
		d = moddate,
		e = accdate)
	)

	# https://stackoverflow.com/questions/25988471/remove-particular-permission-using-os-chmod

	status_perms = stat.S_IMODE(os.lstat(path_temp).st_mode)

	if groupexec(status):
		# change to read/write
		os.chmod(path_temp, status_perms & ~stat.S_IXGRP)
	else:
		# change to read/write/execute
		os.chmod(path_temp, status_perms | stat.S_IXGRP)

	return None


def main(): # main control flow 

	foutput = open("output.txt", "w") # creates or opens with overwrite the output file
	
	File_ls = [] # list for files that need to be manipulated

	if os.path.exists('filelist.txt'): # opens the filelist and reads paths into a list
		with open('filelist.txt') as f:

			for lines in f:
				File_ls.append(lines)

	else:
		foutput.write("filelist.txt can not be found\n") # exits the program if the filelist cannot be found 
		foutput.close()
		sys.exit(0)

	for path in File_ls: # calls gather_and_write on each given path, which will write to output in its block
		try: 
			gather_and_write(foutput, path)

		except FileNotFoundError: # handles missing files (as raised by gather_and_write)
			foutput.write("{} can not be found\n".format(path.strip("\n")))

		except InvalidFileException: 
			foutput.write("{}: Invalid type, Please enter a file\n".format(path.strip("\n")))
				
	foutput.close()
	assert foutput.closed # end of main()


if __name__ == '__main__':
	main()
