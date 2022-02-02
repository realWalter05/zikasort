import os
import argparse
import sys

class File():
	""" Class handles a work with given file"""
	def __init__(self, file, folder, id_file, file_format):
		self.folder = folder
		self.file = file
		self.id = id_file
		self.format = file_format

	def remove_numbers(self):
		return ''.join([i for i in self.file if not i.isdigit()])

	def insert_number(self, file_name):
		file = file_name.split(".")

		file_with_number = file[0] + self.format.format(self.id) + "." + file[1] 
		return file_with_number

	def add_a(self):
		# To prevent file already exists error
		return "a" + self.file

	def rename_as(self, old_name, new_name):
		os.rename(os.path.join(self.folder, self.file), os.path.join(self.folder, new_name))
		self.file = new_name
	

class Sorter():
	""" Class handles a work with given folder """
	def __init__(self, args):
		self.folder = args.folder
		self.file_id = args.file_id if args.file_id else 0
		self.reversed = args.reversed if args.reversed is not None else False
		self.custom_name = args.name if args.name else ""

		if not os.path.isdir(self.folder):
			print(f"Given folder {self.folder} does not exist.")
			return

		self.format_n = "{:0"+str(args.digits_number if args.digits_number else len(str(len(os.listdir(self.folder)))))+"d}"
		
		# Sets the default files
		self.files = []
		file_i = self.file_id
		for file in self.get_folder_files():
			# Get the file
			f = File(file, self.folder, file_i, self.format_n)
			self.files.append(f)
			file_i += 1

		try:
			# Securing that new files have different name than the files in a folder 
			self.add_a_filename()
	
			if self.custom_name:
				self.rename_files_with_name(self.custom_name)
			
			if not self.reversed:
				self.order_files()
			else:
				self.reverse_order_files()

		except PermissionError as e:
			# Handles PermissionErrors
			print(e)
			print(f"You need to start cmd as an administrator to edit folder {self.folder}")

	def get_folder_files(self):
		return os.listdir(self.folder)

	def add_a_filename(self):
		# New file can't overwrite the one in a folder
		for file in self.files:
			file.rename_as(file.file, file.add_a())

	def rename_files_with_name(self, name):
		for file in self.files:
			file.rename_as(file.file, file.insert_number(name + "." + file.file.split(".")[1]))

	def order_files(self):
		for file in self.files:
			file.rename_as(file.file, file.insert_number(file.remove_numbers()))

	def reverse_order_files(self):
		counter = self.file_id
		for file in reversed(self.files):
			file.rename_as(file.file, file.insert_number(file.remove_numbers()))
			counter += 1

def set_argparse():
	parser = argparse.ArgumentParser(description='Reorders/reverses/renames files in a folder.')
	parser.add_argument('folder', metavar='folder', type=str, help='Path to the folder you want reordered.')	
	parser.add_argument('--digits_number', '-d', nargs='?', type=int, help='number of digits the file_id will have (2 - 01, 3 - 001, 3 - 001,...)')
	parser.add_argument('--file_id', '-fid', nargs='?', type=int, help='Defines from which number the sorter will sort the files')
	parser.add_argument('--name', '-n', nargs='?', help='Reorder with a custom name.')
	parser.add_argument('--reversed', '-r', action='store_true', default=False, help='Sorter will reorder the files from the end.')

	return parser.parse_args()

if __name__ == "__main__":
	# Sets the Argpars and runs the Sorter
	Sorter(set_argparse())
