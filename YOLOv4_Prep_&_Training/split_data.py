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
trainfiles=[]
testfiles=[]

# writes to the filename
# each img name in the list imgs
def write_to_file(filename,imgs):
    with open(filename, 'w') as f:
        for img in imgs:
            f.write(img+'\n')

# checks if the given jpeg and its corresponding txt file exist
def txt_and_jpeg(filename,dirpath):
    if('.jpg' in filename):
        txt_name = filename[:(filename.index('.jpg'))]
        txt_name = txt_name+'.txt'
        if(txt_name in os.listdir(dirpath)):
            return True
    else:
        return False

def clth_prep(outerDir,subDir):
    fullpath = outerDir+subDir
    print(os.path.abspath(fullpath))
    files = [os.path.abspath(sys.argv[1]+f) for f in os.listdir(fullpath) if txt_and_jpeg(f,fullpath)]
    split_idx = int(split_pct*len(files))

    training = files[:split_idx]
    testing = files[split_idx:]

    print(subDir+'_test.txt')

    write_to_file(subDir+'_test.txt',testing)
    testfiles.append(subDir+'_test.txt')
    write_to_file(subDir+'_train.txt',training)
    trainfiles.append(subDir+'_train.txt')

def combine_files(flist,name):
    with open(name, 'w') as outfile:
        for fname in flist:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

def main():
    # cli usage info and arg check
    if(len(sys.argv)!=2):
        print("Usage: "+ __file__ + " [directory path]")
        sys.exit(-1)
    
    # get all subdirectories
    clth_cat = [x for x in os.listdir(sys.argv[1]) if x[0]!='.']
    print(clth_cat)

    for cat in clth_cat:
        clth_prep(sys.argv[1],cat)

    print(trainfiles)
    print(testfiles)

    combine_files(testfiles,'test.txt')
    combine_files(trainfiles,'train.txt')

main()