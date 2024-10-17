from pathlib import Path
import os
from .common import formatHex
from .scriptbuilder import ScriptBuilder

class Decoder:

    def decode_text(self, f, builder: ScriptBuilder):
        data = f.read(2)
        # buffer.print(formatHex(data), end=' ')

        number = int.from_bytes(data, byteorder='little')
        # read the next number bytes as the text
        
        origin = f.tell()
        
        byte_sequence = f.read(number)
        try:
            decoded_string = byte_sequence.decode('shift_jis')
            builder.write(decoded_string)
            return True
        except Exception as ex:
            builder.write()
            builder.write(str(ex))
            builder.write(f'{number} bytes at offet {hex(origin)}')
            builder.write()
            builder.write(formatHex(byte_sequence[:100]))
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
        builder = ScriptBuilder()
        # builder._show_offsets = True
        builder.write('# Block offset: ' + hex(pointer))

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
                                builder.write_command(offset, '[VOICE]', args)

                            case b'\x03':
                                args = f.read(3)
                                builder.write_command(offset, '[SFX]', args)

                            case b'\x06':
                                args = f.read(3)
                                builder.write_command(offset, '[BGM]', args)

                            case _:
                                builder.write_byte(offset, b'\x2F', command)

                    case b'\x35':
                        command = f.read(1)
                        match command:
                            case b'\x01':
                                args = f.read(7)
                                builder.write_command(offset, '[SET_BACKGROUND]', args)

                            case _:
                                builder.write_byte(offset, b'\x35', command)

                    case b'\x3C':
                        command = f.read(1)
                        match command:
                            case b'\x00':
                                args = f.read(1)
                                builder.write_command(offset, '[REMOVE_ACTOR]', args)

                            case b'\x01':
                                args = f.read(9)
                                builder.write_command(offset, '[SHOW_ACTOR]', args)

                            # case b'\x0F':
                            #     buffer.print_command(offset, '[3C 0F]')

                            case _:
                                builder.write_byte(offset, b'\x3C', command)

                    case b'\x43':
                        command = f.read(1)
                        # 43 01 - Display Text
                        # 43 02 - Remove Name
                        # 43 03 - Display Name
                        # 43 04 - SCENE
                        # 43 06 - Name: Junichi 
                        match command:
                            case b'\x01':
                                builder.write_command(offset, '[TEXT]', end=' ')
                                hasError = not self.decode_text(f, builder)
                                if hasError: 
                                    break
                                
                            case b'\x02':
                                builder.write_command(offset, '[CLEAR_NAME]')
                                
                            case b'\x03':
                                builder.write_command(offset, '[SET_NAME]', end=' ')
                                hasError = not self.decode_text(f, builder)
                                if hasError: 
                                    break
                                
                            case b'\x04':
                                builder.write_command(offset, '[SCENE]')

                            # case b'\x05':
                            #     buffer.print_command(offset, '[43 05]')
                                
                            case b'\x06':
                                builder.write_command(offset, '[JUNICHI]')

                            case _:
                                builder.write_byte(offset, b'\x43', command)
                                
                    case b'\x46':
                        command = f.read(1)
                        match command:
                            case b'\x00':
                                builder.write_command(offset, '[START-CHOICE]')
                                inChoice = True

                            case b'\x01':
                                if inChoice:
                                    builder.write_command(offset, '[CHOICE]', end=' ')
                                    hasError = not self.decode_text(f, builder)
                                    if hasError: 
                                        break
                                else:
                                    builder.write_byte(offset, b'\x46', command)
                                
                            case b'\x02':
                                if inChoice:
                                    args = f.read(2)
                                    builder.write_offset(offset, '[CHOICE-OFFSET]', args)
                                else:
                                    builder.write_byte(offset, b'\x46', command)

                            case b'\x0F':
                                builder.write_command(offset, '[END-CHOICE]')
                                inChoice = False
                                
                            case _:
                                builder.write_byte(offset, b'\x46', command)
                    case _:
                        builder.write_byte(offset, command, end=' ')

            except Exception as ex:
                print(ex)
                print(hex(f.tell()))
                exit()
                
        return (builder, hasError)

    def read_obj(self, obj_path, script_path):
        """
        Decodes all single .OBJ file to a .TXT file
        
        :param obj_path: The path to the .OBJ file
        :param script_path: The path to the .TXT file
        """        
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
