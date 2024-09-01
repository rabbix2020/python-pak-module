from pak import *
import sys
import os

pak_file = sys.argv[1]
pak_file = pak_file.replace(r"\ "[0], "/")
if not os.path.isfile(pak_file):	exit("There is no such file.")

data = open("PAK1.PAK", "rb").read()

unpack_path = sys.argv[2]
if not os.path.exists(unpack_path):	exit("There is no such directory.")

current_pak = pak(data)

for file in current_pak.files:
   file_path_list = file.name.split('/')
   file_path = ""
   file_path += unpack_path+'/'
   for i in range(len(file_path_list)-1):	file_path+=(file_path_list[i]+"/")
   if not file_path == "" and not os.path.exists(file_path):	os.makedirs(file_path)
   print(file_path+file_path_list[-1])
   open(file_path+file_path_list[-1], "wb").write(data[file.offset:file.offset+file.size])