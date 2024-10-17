import sys
import os, ntpath
from pathlib import Path
from src import Encoder
from src import Manifest

print("DaCapo OBJ Encoder")
print("")

if len(sys.argv) == 3:
    src_path = sys.argv[1]
    obj_path = sys.argv[2]
elif len(sys.argv) == 2:
    if sys.argv[1] == "all":
        src_path = "scripts\\script.manifest"
        obj_path = "obj"
    else:
        src_path = f"scripts\\{sys.argv[1]}.txt"
        obj_path = f"obj\\{sys.argv[1]}.obj"
else:
    print("USAGE: ")
    print("")
    print("Encode all .TXT in .manifest using default folders")
    print("")
    print("   encode all")
    print("")
    print("Encode block1.txt to block1.obj using default folders")
    print("")
    print("   encode block1")
    print("")    
    print("Encode specific .TXT to .OBJ")
    print("")
    print("   encode <path\\to\\script.txt> <path\\to\\block.obj>")
    print("")
    print("Encode all .TXT in specified .manifest to .OBJ using same filename")
    print("")
    print("   encode <path\\to\\script.manifest> <path\\to\\objs>")
    print("")
    exit()

encoder = Encoder()

if src_path.lower().endswith(".manifest"):
    
    manifest = Manifest()
    files = manifest.read(src_path)
    
    Path(obj_path).mkdir(parents=True, exist_ok=True)
    
    for file in files:
        if file.startswith('#'):
            print(f"Skipping {file}")
            continue
        
        buffer = encoder.read_block(file)
        nameext = ntpath.basename(file)
        name = os.path.splitext(nameext)[0] + ".obj"
       
        obj_full_path = os.path.join(obj_path, name)

        # print(file)
        # print(obj_full_path)
        print(f"Encoding {file} to {obj_full_path}")

        with open(obj_full_path, "wb") as f:
             f.write(buffer)

else:
    print(f"Encoding {src_path} to {obj_path}")
    buffer = encoder.read_block(src_path)

    with open(obj_path, "wb") as f:
        f.write(buffer)

print("Done!")