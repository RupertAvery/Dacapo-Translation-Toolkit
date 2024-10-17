
from pathlib import Path
import os, sys

def build_file(file_path, script_path):
    try:
        total_size = 0
        blocks = 0
        sizes = []

        # Collect OBJ file sizes
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
            
        print(f"Writing {blocks} blocks...")
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



print("DaCapo Script Packer")
print("")

if len(sys.argv) == 2:
    file_path = "obj\\script.manifest"
    script_path = sys.argv[1]
elif len(sys.argv) == 3:
    file_path = sys.argv[1]
    script_path = sys.argv[2]
else:
    print("USAGE: ")
    print("")
    print("Pack the files in obj\\script.manifest to the specified .bin")
    print("")
    print("   pack <path\\to\\script.bin>")
    print("")
    print("Pack the files in the specified .manifest to the specified .bin")
    print("")
    print("   pack <path\\to\\script.manifest> <path\\to\\script.bin>")
    print("")
    exit()

build_file(file_path, script_path)

print("Done")
