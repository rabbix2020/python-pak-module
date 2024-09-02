## check this site to understand what's going on -> https://www.gamers.org/dEngine/quake/spec/quake-spec34/qkspec_3.htm#CPAKF

import struct

header_size = 12
class pak_header:
     def __init__(self, id = None, offset = None, size = None):
        self.id = id
        self.offset = offset
        self.size = size

     def read(self, data : bytes):
        if len(data) > header_size:	raise IndexError(f"pak_header.read(): header data cannot be longer than {header_size} bytes")
        self.id = data[:4].decode("ascii")
        if not (self.id == "PACK"):	raise TypeError("pak_header.read(): it's not a PAK file")
        self.offset = struct.unpack("i", data[4:8])[0]
        self.size = struct.unpack("i", data[8:12])[0]

     def pak_header_2_data(self) -> bytes:
        pak_header_data = self.id.encode("ascii")
        pak_header_data += struct.pack("i", self.offset)
        pak_header_data += struct.pack("i", self.size)
        return pak_header_data


entry_size = 64
class pak_entry:
     def __init__(self, name = None, offset = None, size = None):
        self.name = name
        self.offset = offset
        self.size = size

     def read(self, data : bytes):
        if len(data) > entry_size:	raise IndexError(f"pak_entry.read(): entry data cannot be longer than {entry_size} bytes")
        self.name = data[:56]
        if b'\0' in self.name:	self.name = self.name[:self.name.index(b'\0')]
        self.name = self.name.decode('ascii')
        self.offset = struct.unpack("i", data[56:60])[0]
        self.size = struct.unpack("i", data[60:])[0]

     def pak_entry_2_data(self) -> bytes:
        if len(self.name) > 56:	raise IndexError("pak_entry.pak_entry_2_data(): entry name cannot be longer than 56 letters")
        pak_entry_data = self.name.encode("ascii")
        pak_entry_data += bytes([0] * (56-len(self.name)))
        pak_entry_data += struct.pack("i", self.offset)
        pak_entry_data += struct.pack("i", self.size)
        return pak_entry_data

class pak:
     def read_entries(self, pak_head : pak_header, data : list) -> list:
        entries = []
        entries_count = self.entries_count
        for i in range(entries_count):
           current_entry = pak_entry()
           current_entry.read(self.data[pak_head.offset+(i*entry_size):pak_head.offset+((i+1)*entry_size)])
           entries.append(current_entry)

        return entries

     def __init__(self, data : bytes = None):
        if not (data == None):
          self.data = bytes(data)
          self.header : pak_header = pak_header()
          self.header.read(self.data[0:header_size])
          self.entries_count : int = self.header.size // entry_size
          self.entries : list = self.read_entries(self.header, data)
        else:
           self.header = pak_header("PACK", header_size, 0)
           new_data = self.header.pak_header_2_data()
           self.entries_count = 0
           self.entries = list()
           self.data = bytes(new_data)

     def data_from_pak_entry(self, entry : pak_entry):
        return self.data[entry.offset:entry.offset+entry.size]

     def add_file(self, entry_name : str, file_data : bytes):
        new_data = pak_header(self.header.id, self.header.offset+len(file_data), self.header.size+entry_size).pak_header_2_data()
        self.entries_count+=1
        self.header.size+=entry_size
        new_data += self.data[header_size:self.header.offset]
        new_data += file_data
        new_data += self.data[self.header.offset:self.header.offset+((self.entries_count-1) * entry_size)]
        self.header.offset += len(file_data)
        self.entries.append(pak_entry(entry_name, self.header.offset - len(file_data), len(file_data) ))
        new_data += self.entries[-1].pak_entry_2_data()
        self.data = bytes(new_data)