
from pathlib import Path
import os

def extract_block(f, pointer):
    header = f.read(4)
    if header != b'\x4F\x42\x4A\x00':
        print("The file header does not match the expected sequence.")
        exit()
        return

    data = f.read(4)
    size = int.from_bytes(data, byteorder='little')

    f.seek(pointer, 0)
    data = f.read(size)
    return data

    
def build_file(file_path, script_path):
    try:
        total_size = 0
        blocks = 0
        sizes = []
        with open(file_path, "r") as manifest:
            while line := manifest.readline():
                obj_filename = line.strip()
                with open(obj_filename, "rb") as obj:
                    header = obj.read(4)
                    # Verify if the first 4 bytes match 44 43 31 00
                    if header != b'OBJ\x00':
                        print(f"Error reading {obj_filename}")
                        print("The file header does not match the expected sequence.")
                        return
                    file_stats = os.stat(obj_filename)
                    size = file_stats.st_size
                    total_size = total_size + size
                    blocks = blocks + 1
                    sizes.append(size)
                    # obj.seek(0)
                    # data = obj.read(size)
            

        Path("build").mkdir(parents=True, exist_ok=True)

        # There is a dummy pointer that points to the end of file
        # the header is 16 bytes
        pointer_start = blocks * 4 + 16 + 4
        pointer = pointer_start 
        size = total_size + pointer_start
        sizebytes = size.to_bytes(4, 'little')

        with open(script_path, "wb") as script:
            # Write the header
            script.write(b'\x44\x43\x31\x00')   # DC1\x00
            script.write(b'\x00\x00\x00\x00')
            script.write(sizebytes)             # file size
            script.write(b'\x01\x00\x00\x00')   # unknown
            
            script.write(pointer_start.to_bytes(4, 'little'))
            for size in sizes:
                pointer = pointer + size
                script.write(pointer.to_bytes(4, 'little'))

            with open(file_path, "r") as manifest:
                while line := manifest.readline():
                    obj_filename = line.strip()
                    with open(obj_filename, "rb") as obj:
                        data = obj.read()
                        script.write(data)

    except FileNotFoundError:
        print("The specified file was not found.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

file_path = "obj/script.manifest"
script_path = "build/script.bin"
build_file(file_path, script_path)
