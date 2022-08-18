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

def main():

	# create output file - !!!

	foutput = open("output.txt", "w")

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

			#st_mode



			print(status.st_mode)

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
