'''
this script will create two files
1. test.txt
2. train.txt
for yolov3
these files will contain the names of the files to be
used for training and testing
'''

import os, sys
split_pct = 0.75

# writes to the filename
# each img name in the list imgs
def write_to_file(filename,imgs):
    with open(filename, 'w') as f:
        for img in imgs:
            f.write(img+'\n')

def main():
    if(len(sys.argv)!=2):
        print("Usage: "+ __file__ + " [directory path]")
        sys.exit(-1)
    
    files = [f for f in os.listdir(sys.argv[1]) if ".jpg" in f]
    split_idx = int(split_pct*len(files))
    
    training = files[:split_idx]
    testing = files[split_idx:]

    write_to_file('test.txt',testing)
    write_to_file('train.txt',training)
    

main()