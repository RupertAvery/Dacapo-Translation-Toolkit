import sys, os, ntpath
from pathlib import Path 
from src import Decoder

"""
Da Capo I&II- Plus Situation Portable 
Decodes an .obj file into a script .txt file
"""

def read_manifest(decoder: Decoder, src_path, script_path):
    """
    Decodes all the .OBJ files listed in a .MANIFEST file
    
    :param src_path: The path to the .MANIFEST file
    :param script_path: The path where the decoded .TXT files will be placed
    """
    
    Path(script_path).mkdir(parents=True, exist_ok=True)
    
    scripts = []
    scripts_manifest = os.path.join(script_path, "script.manifest")
    
    if len(os.listdir(script_path)) != 0:
        print("The target directory is not empty. Are you sure you want to overwrite it?")
        response = input()
        if response.lower() != "y":
            exit()
    
    src_dir = os.path.dirname(src_path)

    with open(src_path, "r") as manifest:

        while line := manifest.readline():

            obj_filename = line.strip()
            
            nameext = ntpath.basename(obj_filename)
            
            fname = os.path.splitext(nameext)[0]

            name = fname + ".txt"
            
            if fname == "block213" or fname == "block222" or fname == "block832":
                scripts.append("# " + name)
            else:
                scripts.append(name)
            
            script_full_path = os.path.join(script_path, name)
            
            obj_path = os.path.join(src_dir, obj_filename)
            
            print(f"Decoding {obj_path} to {script_full_path}")
            
            decoder.read_obj(obj_path, script_full_path)

    print("Writing script.manifest")

    with open(scripts_manifest, "w") as manifest:
        
        for script in scripts:
            
            manifest.write(script + '\n')


print("DaCapo OBJ Decoder")
print("")

if len(sys.argv) == 3:
    src_path = sys.argv[1]
    script_path = sys.argv[2]
elif len(sys.argv) == 2:
    if sys.argv[1] == "all":
        src_path = "obj\\script.manifest"
        script_path = "scripts"
    else:
        src_path = f"obj\\{sys.argv[1]}.obj"
        script_path = f"scripts\\{sys.argv[1]}.txt"    
else:
    print("USAGE: ")
    print("")
    print("Decode all .obj in .manifest using default folders")
    print("")
    print("   decode all")
    print("")
    print("Decode block1.obj to block1.txt using default folders")
    print("")
    print("   decode block1")
    print("")
    print("Decode specific .obj to specific .txt")
    print("")
    print("   decode <path\\to\\block.obj> <path\\to\\script.txt>")
    print("")
    print("Decode all .obj in specific .manifest to specified output folder")
    print("")
    print("   decode <path\\to\\script.manifest> <path\\to\\scripts>")
    print("")
    exit()
    
decoder = Decoder()

if src_path.lower().endswith(".manifest"):
    read_manifest(decoder, src_path, script_path)
else:
    print(f"Decoding {src_path} to {script_path}")

    script_dir = os.path.dirname(script_path)    
    Path(script_dir).mkdir(parents=True, exist_ok=True)
        
    decoder.read_obj(src_path, script_path)



print("Done!")

