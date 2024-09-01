import struct
from random import random

class pak_header:
     def __init__(self):
        self.id = None
        self.offet = None
        self.size = None
     def read(self, data : list):
        self.id = data[:4].decode("ascii")
        if not (self.id == "PACK"):	raise TypeError("pak_header.read(): it's not a PAK file")
        self.offset = struct.unpack("i", data[4:8])[0]
        self.size = struct.unpack("i", data[8:12])[0]


entry_size = 64
class pak_entry:
     def __init__(self):
        self.name = None
        self.offset = None
        self.size = None

class pak:
     def read_files(self, pak_head : pak_header, data : list):
        files = []
        files_count = self.files_count
        for i in range(files_count):
           current_entry = pak_entry()

           entry_name = data[pak_head.offset+i*entry_size:pak_head.offset+i*entry_size+56]
           if b'\0' in entry_name:	entry_name = entry_name[:entry_name.index(b'\0')]
           current_entry.name = entry_name.decode('ascii')
           current_entry.offset = struct.unpack("i", data[pak_head.offset+i*entry_size+56:pak_head.offset+i*entry_size+60])[0]
           current_entry.size = struct.unpack("i", data[pak_head.offset+i*entry_size+60:pak_head.offset+i*entry_size+64])[0]
           files.append(current_entry)

        return files

     def __init__(self, data):
        self.data = data
        self.header : pak_header = pak_header()
        self.header.read(data)
        self.files_count = self.header.size // entry_size
        self.files : list = self.read_files(self.header, data);
