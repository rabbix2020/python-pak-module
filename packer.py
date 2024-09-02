from pak import *
import sys
import os

unpack_path = sys.argv[1]
unpack_path = unpack_path.replace(r"\ "[0], "/")
if not os.path.exists(unpack_path):	exit("There is no such directory.")

pak_file = sys.argv[2]
pak_file = pak_file.replace(r"\ "[0], "/")

current_pak = pak()

for path, subdirs, files in os.walk(unpack_path):
    for name in files:
        file_path = os.path.join(path, name).replace(r"\ "[0], "/")
        file_data = open(file_path, "rb").read()
        file_path = file_path.replace(unpack_path+'/', "")
        print(file_path)
        current_pak.add_file(file_path, file_data)

open(pak_file, "wb").write(current_pak.data)