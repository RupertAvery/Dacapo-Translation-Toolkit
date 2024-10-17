# script.bin

 Name          | Size (bytes)         |  Contents/Description             
---------------|----------------------|------------------------           
 Magic         | 4                    |  `DC1\0`                          
 Empty         | 4                    |  `\0`                             
 File Size     | 4                    |  Size of file                     
 Unknown       | 4                    |  `\x01\x00\x00\x00`               
 Pointers      | 4 * # of blocks + 1  |  list of offsets to each block 
 OBJs          |                      |  embedded OBJ files 

# OBJ / block

 Name          | Size (bytes)         |  Contents/Description             
---------------|----------------------|------------------------           
 Magic         | 4                    |  `OBJ\0`                          
 Size          | 4                    |  Size of block / file
 Empty         | 4                    |  `\x00\x00\x00\x00`               
 Bytecode      |                      |   
