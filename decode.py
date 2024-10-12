from pathlib import Path
import sys, os, ntpath

"""
Da Capo I&II- Plus Situation Portable 
Decodes an .obj file into a script .txt file
"""

class LabelOffset:
    _label = None
    _offset = None

class StringBuilder:
    _file_str = None
    _byte_buf = None
    _show_offsets = False
    _byte_start = True
    _byte_offset = 0
    _offsets = []
    _offset_index = 1

    def __init__(self):
        self._file_str = ''
        self._byte_buf = ''
        
    def print(self, str = '', args = '', end = '\n'):
        self._file_str = self._file_str + str + end

    def __check_labels__(self, offset):
        for _offset in self._offsets:
            if _offset._offset == offset:
                self._file_str = self._file_str + '[LABEL] ' + _offset._label + '\n'
                
        
    def __flush_bytes__(self):
        if len(self._byte_buf) > 0:
            if self._byte_start and self._show_offsets:
                self._file_str = self._file_str + hex(self._byte_offset) + ': '
            self._file_str = self._file_str + '[BYTES] ' + self._byte_buf + '\n'
            self._byte_buf = ''
        self._byte_start = True

    def print_jump(self, offset, str, label_offset, end = '\n'):
        self.__flush_bytes__()
        target_offset = int.from_bytes(label_offset, byteorder='little')

        jump_offset = LabelOffset()
        jump_offset._offset = offset + target_offset
        jump_offset._label = f"Label{self._offset_index}"

        self._offset_index = self._offset_index + 1

        self._offsets.append(jump_offset)

        if self._show_offsets:
            self._file_str = self._file_str + hex(offset) + ': '

        self._file_str = self._file_str + str + ' ' + jump_offset._label + end

        pass
    
    def print_command(self, offset, str = '', args = None, end = '\n'):
        self.__flush_bytes__()
        self.__check_labels__(offset)
        
        if self._show_offsets:
            self._file_str = self._file_str + hex(offset) + ': '

        self._file_str = self._file_str + str 

        if args != None:
            self._file_str = self._file_str + ' ' + formatHex(args) 

        self._file_str = self._file_str + end 

    def print_byte(self, offset, bytes, args = None, end = ' '):
        if self._byte_start:
            self._byte_offset = offset

        self.__check_labels__(offset)
        
        self._byte_buf = self._byte_buf + formatHex(bytes)

        if args != None:
            self._byte_buf = self._byte_buf + ' ' + formatHex(args) 

        self._byte_buf = self._byte_buf + end 

        self._byte_start = False

    def __str__(self):
        self.__flush_bytes__()
        return self._file_str

    def value(self):
        self.__flush_bytes__()
        return self._file_str     

def formatHex(data):
    return ' '.join('{:02X}'.format(x) for x in data)

class Decoder:

    def decode_text(self, f, buffer: StringBuilder):
        data = f.read(2)
        # buffer.print(formatHex(data), end=' ')

        number = int.from_bytes(data, byteorder='little')
        # read the next number bytes as the text
        
        origin = f.tell()
        
        byte_sequence = f.read(number)
        try:
            decoded_string = byte_sequence.decode('shift_jis')
            buffer.print(decoded_string)
            return True
        except Exception as ex:
            buffer.print()
            buffer.print(str(ex))
            buffer.print(f'{number} bytes at offet {hex(origin)}')
            buffer.print()
            buffer.print(formatHex(byte_sequence[:100]))
            return False

    def decode_block(self, f, pointer, block):
        print(hex(pointer))
        f.seek(pointer, 0)
        
        (buffer, hasError) = self.decode_obj(f, pointer)
        
        Path("scripts").mkdir(parents=True, exist_ok=True)
        Path("error").mkdir(parents=True, exist_ok=True)
            
        folder = 'error' if hasError else 'scripts'    
        file_path = f'{folder}/block {block}.txt'
        
        with open(file_path, "w",  encoding='utf8') as out:
            out.write(buffer.value())
        

    def decode_obj(self, f, pointer):
        buffer = StringBuilder()
        buffer.print('# Block offset: ' + hex(pointer))

        f.seek(pointer, 0)
        
        header = f.read(4)
        
        if header != b'\x4F\x42\x4A\x00':
            print("The file header does not match the expected sequence.")
            exit()
            return

        data = f.read(4)
        size = int.from_bytes(data, byteorder='little')
        
        end = pointer + size

        hasError = False
        inChoice = False
        
        while f.tell() < end:
            try:
                offset = f.tell()
                command = f.read(1)

                match command:
                    case b'\x2F':
                        command = f.read(1)
                        match command:
                            case b'\x00':
                                args = f.read(3)
                                buffer.print_command(offset, '[VOICE]', args)

                            case b'\x03':
                                args = f.read(3)
                                buffer.print_command(offset, '[SFX]', args)

                            case b'\x06':
                                args = f.read(3)
                                buffer.print_command(offset, '[BGM]', args)

                            case _:
                                buffer.print_byte(offset, b'\x2F', command)

                    case b'\x35':
                        command = f.read(1)
                        match command:
                            case b'\x01':
                                args = f.read(7)
                                buffer.print_command(offset, '[SET_BACKGROUND]', args)

                            case _:
                                buffer.print_byte(offset, b'\x35', command)

                    case b'\x3C':
                        command = f.read(1)
                        match command:
                            case b'\x00':
                                args = f.read(1)
                                buffer.print_command(offset, '[REMOVE_ACTOR]', args)

                            case b'\x01':
                                args = f.read(9)
                                buffer.print_command(offset, '[SHOW_ACTOR]', args)

                            # case b'\x0F':
                            #     buffer.print_command(offset, '[3C 0F]')

                            case _:
                                buffer.print_byte(offset, b'\x3C', command)

                    case b'\x43':
                        command = f.read(1)
                        # 43 01 - Display Text
                        # 43 02 - Remove Name
                        # 43 03 - Display Name
                        # 43 04 - SCENE
                        # 43 06 - Name: Junichi 
                        match command:
                            case b'\x01':
                                buffer.print_command(offset, '[TEXT]', end=' ')
                                hasError = not self.decode_text(f, buffer)
                                if hasError: 
                                    break
                                
                            case b'\x02':
                                buffer.print_command(offset, '[CLEAR_NAME]')
                                
                            case b'\x03':
                                buffer.print_command(offset, '[SET_NAME]', end=' ')
                                hasError = not self.decode_text(f, buffer)
                                if hasError: 
                                    break
                                
                            case b'\x04':
                                buffer.print_command(offset, '[SCENE]')

                            # case b'\x05':
                            #     buffer.print_command(offset, '[43 05]')
                                
                            case b'\x06':
                                buffer.print_command(offset, '[JUNICHI]')

                            case _:
                                buffer.print_byte(offset, b'\x43', command)
                                
                    case b'\x46':
                        command = f.read(1)
                        match command:
                            case b'\x00':
                                buffer.print_command(offset, '[START-CHOICE]')
                                inChoice = True

                            case b'\x01':
                                if inChoice:
                                    buffer.print_command(offset, '[CHOICE]', end=' ')
                                    hasError = not self.decode_text(f, buffer)
                                    if hasError: 
                                        break
                                else:
                                    buffer.print_byte(offset, b'\x46', command)
                                
                            case b'\x02':
                                if inChoice:
                                    args = f.read(2)
                                    buffer.print_jump(offset, '[CHOICE-OFFSET]', args)
                                else:
                                    buffer.print_byte(offset, b'\x46', command)

                            case b'\x0F':
                                buffer.print_command(offset, '[END-CHOICE]')
                                inChoice = False
                                
                            case _:
                                buffer.print_byte(offset, b'\x46', command)
                    case _:
                        buffer.print_byte(offset, command, end=' ')

            except Exception as ex:
                print(ex)
                print(hex(f.tell()))
                exit()
                
        return (buffer, hasError)

    def read_manifest(self, src_path, script_path):
        with open(src_path, "r") as manifest:
            while line := manifest.readline():
                obj_filename = line.strip()
                
                nameext = ntpath.basename(obj_filename)
                
                name = os.path.splitext(nameext)[0] + ".txt"
                
                script_full_path = os.path.join(script_path, name)
                
                self.read_obj(obj_filename, script_full_path)

    def read_obj(self, obj_path, script_path):
        print(f"Decoding {obj_path}")
        
        with open(obj_path, "rb") as f:
            (buffer, hasError) = self.decode_obj(f, 0)
            
            script_dir = os.path.dirname(script_path)
            
            Path(script_dir).mkdir(parents=True, exist_ok=True)
            
            with open(script_path, "w",  encoding='utf8') as out:
                out.write(buffer.value())

    def read_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                # Read the first 4 bytes
                header = f.read(4)
                
                # Verify if the first 4 bytes match 44 43 31 00
                if header != b'\x44\x43\x31\x00':
                    print("The file header does not match the expected sequence.")
                    return

                print("Header matched successfully!")
                
                # Skip the next 4 bytes
                f.seek(4, 1)

                # Read the next 4 bytes and interpret them as a 16-bit number in little endian
                data = f.read(4)
                number = int.from_bytes(data, byteorder='little')

                # Size of file
                # print(hex(number))
                f.seek(4, 1)
            
                start = 0
                
                pointers = []
                
                i = 0
                while start == 0 or f.tell() < start:
                    data = f.read(4)
                    number = int.from_bytes(data, byteorder='little')
                    if start == 0:
                        start = number
                    pointers.append(number)
                    i = i + 1

                block = 1
                for p in pointers:
                    self.decode_block(f, p, block)
                    block = block + 1

        except FileNotFoundError:
            print("The specified file was not found.")
            
        except Exception as e:
            print(f"An error occurred: {e}")

print("DaCapo OBJ Decoder")
print("==================")

if len(sys.argv) == 3:
    src_path = sys.argv[1]
    script_path = sys.argv[2]
else:
    print("USAGE: ")
    print("")
    print("Decode one .OBJ")
    print("")
    print("   decode <path/to/block.obj> <path/to/script.txt>")
    print("")
    print("Decode all .OBJ in .manifest")
    print("")
    print("   decode <path/to/script.manifest> <path/to/scripts>")
    print("")
    exit()

decoder = Decoder()

if src_path.lower().endswith(".manifest"):
    decoder.read_manifest(src_path, script_path)
else:
    decoder.read_obj(src_path, script_path)



print("Done!")

