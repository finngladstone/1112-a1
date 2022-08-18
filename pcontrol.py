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
		print("Filelist.txt not found")

	for path in File_ls:
		# remove newline char from path
		path = path.strip("\n")

		try:
			status = os.stat(path)

			foutput.write(path + " Group Readable: " + str(groupread(status)) + ", Group Executable: " + str(groupexec(status)) + " ")
			foutput.write("Size: {a}, Owner: {b}, Group: {c}, last modified date: {d}, last access date: {e}\n".format(
				a = status.st_size,
				b = status.st_uid,
				c = status.st_gid,
				d = status.st_mtime,
				e = status.st_atime)
			)

			if groupexec(status):
				# change to not execute
				os.chmod(path, stat.S_IWGRP)
				print("changed to read/write")
			else:
				# change to execute
				os.chmod(path, stat.S_IXGRP)
				print("changed to exec")




			# Group Readable: {True/False}, Group Executable: {True/False}”
			# “Size: {}, Owner: {}, Group: {}, last modified date: {}, last access date: {}”
			# see https://www.geeksforgeeks.org/python-os-stat-method/
			# make modifications
			# write in output
			pass

		except FileNotFoundError:
			print("File not found")
			pass


	foutput.close()
	assert foutput.closed




if __name__ == '__main__':
	main()
