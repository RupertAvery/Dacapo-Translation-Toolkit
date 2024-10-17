
import sys, os
from pathlib import Path

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

    
def read_file(file_path, obj_dir = "obj"):
    pointers = []
    block = 1
    try:
        with open(file_path, "rb") as f:
            # Read the first 4 bytes
            header = f.read(4)
            
            # Verify if the first 4 bytes match 44 43 31 00
            if header != b'\x44\x43\x31\x00':
                print("The file header does not match the expected sequence.")
                return
            
            # Skip the next 4 bytes
            f.seek(4, 1)

            # Read the next 4 bytes and interpret them as a 16-bit number in little endian
            data = f.read(4)
            end_marker = int.from_bytes(data, byteorder='little')

            # Size of file
            # print(hex(number))
            f.seek(4, 1)
        
            start = 0
            
            i = 0
            while start == 0 or f.tell() < start:
                data = f.read(4)

                number = int.from_bytes(data, byteorder='little')

                if start == 0:
                    start = number

                if number != end_marker:
                    pointers.append(number)

                i = i + 1

            Path(obj_dir).mkdir(parents=True, exist_ok=True)
            
            manifest_path = os.path.join(obj_dir, "script.manifest")

            with open(manifest_path, "w") as manifest:
                
                for p in pointers:

                    data = extract_block(f, p)

                    obj_filename = f"block{block}.obj"

                    obj_path = os.path.join(obj_dir, obj_filename)
                    
                    with open(obj_path, "wb") as obj:

                        obj.write(data)

                    manifest.write(obj_filename + '\n')

                    block = block + 1

    except FileNotFoundError:
        print("The specified file was not found.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return len(pointers)

print("DaCapo Script Unpacker")
print("")

if len(sys.argv) == 1:
    file_path = "script.bin"
    obj_path = "obj"
elif len(sys.argv) == 2:
    file_path = sys.argv[1]
    obj_path = "obj"
elif len(sys.argv) == 2:
    file_path = sys.argv[1]
    obj_path = sys.argv[2]
else:
    print("USAGE: ")
    print("")
    print("   unpack")
    print("")
    print("")
    print("   unpack <path\\to\\script.bin>")
    print("")
    print("")
    print("   unpack <path\\to\\script.bin> <path\\to\\obj>")
    print("")
    exit()


print(f"Unpacking {file_path} to {obj_path}")

blocks = read_file(file_path, obj_path)

print(f"{blocks} blocks unpacked")