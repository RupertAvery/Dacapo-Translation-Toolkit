import struct
import typing

class DataStream(bytearray):

    def append(self, v, fmt='>B'):
        self.extend(struct.pack(fmt, v))
        
def process(f: typing.IO, line: str):
    if line.startswith("#"):
        return None
      
    elif line.startswith("[BYTES]"):
        line = line[8:]
        line = line.strip()
        return bytearray.fromhex(line)

# 2F XX    
    elif line.startswith("[VOICE]"):
        line = line[8:]
        line = line.strip()
        buffer = bytearray(b'\x2F\x00')
        buffer.extend(bytearray.fromhex(line))
        return buffer 

    elif line.startswith("[SFX]"):
        line = line[6:]
        line = line.strip()
        buffer = bytearray(b'\x2F\x03')
        buffer.extend(bytearray.fromhex(line))
        return buffer 
    
    elif line.startswith("[BGM]"):
        line = line[6:]
        line = line.strip()
        buffer = bytearray(b'\x2F\x06')
        buffer.extend(bytearray.fromhex(line))
        return buffer 


# 35 XX    
    elif line.startswith("[SET_BACKGROUND]"):
        line = line[17:]
        line = line.strip()
        buffer = bytearray(b'\x35\x01')
        buffer.extend(bytearray.fromhex(line))
        return buffer 

# 3C XX    
    elif line.startswith("[REMOVE_ACTOR]"):
        line = line[15:]
        line = line.strip()
        buffer = bytearray(b'\x3C\x00')
        buffer.extend(bytearray.fromhex(line))
        return buffer 

    elif line.startswith("[SHOW_ACTOR]"):
        line = line[13:]
        line = line.strip()
        buffer = bytearray(b'\x3C\x01')
        buffer.extend(bytearray.fromhex(line))
        return buffer 
        
# 43 XX    
    elif line.startswith("[TEXT]"):
        line = line[7:]
        buffer = bytearray()
        buffer.extend(line.encode('shiftjis'))
        ptr = f.tell()
        line = f.readline()
        while not line.startswith("["):
            if line != '\n':
                buffer.extend(line.encode('shiftjis'))
            line = f.readline()
        f.seek(ptr, 0)
        
        size = len(buffer)
        sizebytes = size.to_bytes(2, 'little')

        textbuffer = bytearray(b'\x43\x01')
        textbuffer.extend(sizebytes)
        textbuffer.extend(buffer)
        
        return textbuffer

    elif line.startswith("[CLEAR_NAME]"):
        return bytearray(b'\x43\x02')
    
    elif line.startswith("[SET_NAME]"):
        line = line[11:]
        line = line.strip()
        buffer = bytearray()
        buffer.extend(line.encode('shiftjis'))
        
        size = len(buffer)
        sizebytes = size.to_bytes(2, 'little')

        textbuffer = bytearray(b'\x43\x03')
        textbuffer.extend(sizebytes)
        textbuffer.extend(buffer)
        
        return textbuffer    
        
    elif line.startswith("[SCENE]"):
        return bytearray(b'\x43\x04')

    elif line.startswith("[JUNICHI]"):
        return bytearray(b'\x43\x06')

# 46 XX

    elif line.startswith("[START-CHOICE]"):
        return bytearray(b'\x46\x00')

    elif line.startswith("[CHOICE]"):
        line = line[9:]
        buffer = bytearray()
        buffer.extend(line.encode('shiftjis'))
        ptr = f.tell()
        line = f.readline()
        while not line.startswith("["):
            if line != '\n':
                buffer.extend(line.encode('shiftjis'))
            line = f.readline()
        f.seek(ptr, 0)
        
        size = len(buffer)
        sizebytes = size.to_bytes(2, 'little')

        textbuffer = bytearray(b'\x46\x01')
        textbuffer.extend(sizebytes)
        textbuffer.extend(buffer)
        
        return textbuffer    


    elif line.startswith("[JUMP-TO]"):
        line = line[10:]
        line = line.strip()
        buffer = bytearray(b'\x46\x02')
        buffer.extend(bytearray.fromhex(line))
        return buffer
    
    elif line.startswith("[END-CHOICE]"):
        return bytearray(b'\x46\x0F')

    elif line.startswith("#"):
        return None


def read_block(file_path):
    buffer = bytearray()
    try:
        with open(file_path, "r", encoding="utf8") as f:
            i = 0
            while line := f.readline():
                i = i + 1
                print(line)
                data = process(f, line)
                if data != None:
                    buffer.extend(data)
            print(f'{i} lines parsed')

    except FileNotFoundError:
        print("The specified file was not found.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

    size = len(buffer) + 8
    sizebytes = size.to_bytes(4, 'little')
    textbuffer = bytearray(b'\x4F\x42\x4A\x00')
    textbuffer.extend(sizebytes)
    textbuffer.extend(buffer)
                
    return textbuffer


file_path = "scripts/block 3.txt"
buffer = read_block(file_path)

with open("block 3.bin", "wb") as f:
    f.write(buffer)