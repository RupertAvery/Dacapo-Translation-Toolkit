import typing, sys, traceback

class ChoiceOffset:
    _label = None
    _offset = None

class Encoder:
    _offsets = []
    
    def __init__(self):
        self._offsets = []
                
    def process(self, f: typing.IO, line: str, target: bytearray):
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


        elif line.startswith("[CHOICE-OFFSET]"):
            line = line[16:]
            line = line.strip()
                
            choice_offset = ChoiceOffset()
            choice_offset._offset = len(target) + 2
            choice_offset._label = line

            self._offsets.append(choice_offset)
            
            buffer = bytearray(b'\x46\x02\x00\x00')
            
            return buffer
        
        elif line.startswith("[END-CHOICE]"):
            return bytearray(b'\x46\x0F')

        elif line.startswith("[LABEL]"):
            line = line[8:]
            line = line.strip()
            position = len(target)
           
            for _offset in self._offsets:
                if _offset._label == line:
                    offset = position - _offset._offset + 2
                    offset_bytes = offset.to_bytes(2, 'little')
                    target[_offset._offset] = offset_bytes[0]
                    target[_offset._offset + 1] = offset_bytes[1]
                
    # TODO: move this out so it can be called multiple times
    # without having to reset the state
    def read_block(self, file_path):
        buffer = bytearray()
        try:
            with open(file_path, "r", encoding="utf8") as f:
                i = 0
                self._offsets = []
                while line := f.readline():
                    i = i + 1
                    # print(line)
                    data = self.process(f, line, buffer)
                    if data != None:
                        buffer.extend(data)
                        
                print(f'{i} lines parsed')

        except FileNotFoundError:
            print("The specified file was not found.")
            
        except Exception as e:  
            print(f"An error occurred in {file_path}:")
            print(f"{e}")
            traceback.print_tb(e.__traceback__, limit=10, file=sys.stdout)          

        size = len(buffer) + 8
        sizebytes = size.to_bytes(4, 'little')
        textbuffer = bytearray(b'\x4F\x42\x4A\x00')
        textbuffer.extend(sizebytes)
        textbuffer.extend(buffer)
                    
        return textbuffer
