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

import sys

def main():

	# list for files that need to be manipulated
	File_ls = []

	try: # loops through lines and adds addresses to file ls
		with open('filelist.txt') as f:
			for lines in f:
				File_ls.append(lines)

		assert f.closed

	except FileNotFoundError:
		print("Filelist.txt not found")

	for file_address in File_ls:

		try:
			# make modifications
			# write in output
			pass

		except FileNotFoundError:
			# write to output
			pass





if __name__ == '__main__':
	main()
