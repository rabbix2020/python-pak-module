from pak import *
import sys
import os

pak_file = sys.argv[1]
pak_file = pak_file.replace(r"\ "[0], "/")
if not os.path.isfile(pak_file):	exit("There is no such file.")

data = open(pak_file, "rb").read()

unpack_path = sys.argv[2]
unpack_path = unpack_path.replace(r"\ "[0], "/")
if not os.path.exists(unpack_path):	exit("There is no such directory.")

current_pak = pak(data)

for entry in current_pak.entries:
   file_path_list = entry.name.split('/')
   file_path = ""
   file_path += unpack_path+'/'
   for i in range(len(file_path_list)-1):	file_path+=(file_path_list[i]+"/")
   if not file_path == "" and not os.path.exists(file_path):	os.makedirs(file_path)
   print(file_path+file_path_list[-1])
   open(file_path+file_path_list[-1], "wb").write(current_pak.data_from_pak_entry(entry))