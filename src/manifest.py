import os

class Manifest:
    
    def read(self, src_path):
        files = []

        with open(src_path, "r") as manifest:
            while line := manifest.readline():
                filename = line.strip()
                src = os.path.dirname(src_path)
                
                full_path = os.path.join(src, filename)
                files.append(full_path)
                
        return files

    def write(self, files, target_path):
        
        with open(target_path, "w") as manifest:
            while file := files:
                manifest.write(file + '\n')