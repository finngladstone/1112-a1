# Allowed:
#
# os
#
# os.chmod: #106
# os.stat: #106
# os.path: #103
#
# os.access: #118
# time: #100
#
# datetime: #112
# grp: #100
# pwd: #100
#
# stat: #115

import os

import sys
import stat

from datetime import datetime

import grp, pwd

def main():

	foutput = open("output.txt", "w") # creates or opens with overwrite the output file

	# function definitions for perms checks later

	# https://stackoverflow.com/a/1861859

	def groupread(status):
		return bool(status.st_mode & stat.S_IRGRP)

	def groupexec(status):
		return bool(status.st_mode & stat.S_IXGRP)

	# list for files that need to be manipulated
	File_ls = []

	try: # loops through lines and adds addresses to file ls
		with open('filelist.txt') as f:
			for lines in f:
				File_ls.append(lines)

		assert f.closed

	except FileNotFoundError:
		# write error code to output and exit program 
		foutput.write("filelist.txt can not be found\n")
		foutput.close()
		sys.exit(0)

	for path in File_ls:
		# remove newline char from path
		path_temp = path.strip("\n")
		path_temp = os.path.abspath(path_temp)

		try:
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

			if groupexec(status):
				# change to read/write
				os.chmod(path_temp, stat.S_IRGRP | stat.S_IWGRP)
			else:
				# change to read/write/execute
				os.chmod(path_temp, stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP)

		except FileNotFoundError:
			foutput.write("{} can not be found\n".format(path.strip("\n")))
			pass


	foutput.close()
	assert foutput.closed




if __name__ == '__main__':
	main()
