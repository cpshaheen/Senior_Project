# load and prepare deepfashion dataset and save to file

# TO USE:
# provide attrs_map.json file as the first argument and 
# 'imgs_attrs_map.json' as the second argument with the optional
# -s flag at the end of the command followed by the desired max set size

import json, sys
from os import listdir
from numpy import zeros
from numpy import asarray
from numpy import savez_compressed
from numpy import savez
from numpy import load
from pandas import read_csv
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from datetime import date

today = date.today()

attr_count = {}

# one hot enc for list of tags 
def one_hot_enc(tags, mapping):
    # create empty vector
    enc = zeros(len(mapping), dtype = 'uint8')
    # mark 1 for each tag in the vector
    for tag in tags:
        enc[mapping[tag]] = 1
    return enc

# makes sure that attributes are not over represented in data
# returning a 0 indicates that there this image contains an over
# representative class and should be passed over
def balancer(tags):
    for tag in tags:
        if attr_count[tag]>750:
            return 0
    for tag in tags:
        attr_count[tag] += 1
    return 1

# load images into memory
def load_dataset(file_mapping, tag_mapping, ds_size):
    photos, targets = list(), list()

    i = 0

    for fname, tags in file_mapping.items():
        print(f" {((i/ds_size)*100):.0f} % complete", sep=' ', end='\r', flush=True)
        # print(str(i/total_len) + '% complete', end='', flush=True)

        # load the image
        photo = load_img(fname, target_size=(320,400))
        photo = img_to_array(photo, dtype = 'uint8')
        # load its
        tags = file_mapping[fname]

        if balancer(tags) == 0:
            continue

        target = one_hot_enc(tags, tag_mapping)
        photos.append(photo)
        targets.append(target)
        
        i+=1
        
        if i == ds_size:
            break

    X = asarray(photos, dtype='uint8')
    Y = asarray(targets, dtype='uint8')
    return X,Y

def main():
    # check for command line flag
    if(len(sys.argv)==5 and sys.argv[3]=='-s'):
        size = int(sys.argv[4])
    else:
        size = 20000

    print(f"Producing data set with {size} images")

    # load mappings
    f = open(sys.argv[1], 'r')
    attrs_map = json.load(f)
    f.close()

    for key in attrs_map.keys():
        attr_count[key] = 0
    
    print(attr_count)
    
    f = open(sys.argv[2], 'r')
    imgs_map = json.load(f)
    f.close()

    # load images and labels 
    X, y = load_dataset(imgs_map,attrs_map,size)
    print(X.shape, y.shape)

    with open('metadata_'+ today.strftime("%m-%d-%y") +'.txt', 'w') as md:
        json.dump(attr_count, md)

    # save arrays of images and their corresponding labels
    savez('macys_data_'+today.strftime("%m-%d-%y")+'.npz', X, y)

main()