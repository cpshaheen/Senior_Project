import sys, json, os
from datetime import date

today = date.today()
# this script takes the list of given attributes provided 
# as the first cli argument and finds images that contain at least one
# of those attributes. it also merges similar attributes to limit
# the number of classes for simplicity sake

def make_attr_map(dirs, attr_dict):
    # create a mapping of images to their attributes
    # first check for attributes in their directory name 
    # (ie hood in hoodies)
    # then check the image name for the attributes
    attr_imgs = []
    # iterate through subdirs
    for dir in dirs:
        pre_attrs = []
        # create a copy of the dict to prevent ref mutation
        attrs = attr_dict.keys()
        # iterate through attributes
        for attr in attrs:
            if attr in dir.lower():
                pre_attrs.append(attr_dict[attr])
    
        imgs = [x for x in os.listdir(dir) if '.jpg' in x]
        # iterate through images in the dir
        for img in imgs:
            img_attrs = pre_attrs.copy()
            for attr in attrs:
                if attr in img.lower() and not(attr_dict[attr] in img_attrs):
                    img_attrs.append(attr_dict[attr])
            if len(img_attrs)>0:
                attr_imgs.append([dir+'/'+img,img_attrs])
    
    # saving the images and their attributes to a json file
    f = open('macys_img_attrs_'+ today.strftime("%m-%d-%y") +'.json', 'w')
    print(len(attr_imgs))
    json.dump(attr_imgs, f)
    f.close()

def get_attr_dict(attr_list):
    # read in the desired list of attribute
    f = open(attr_list, 'r')
    des = f.readlines()[2:]
    f.close()

    # create a dictionary of attributes where
    # the keys are the strings sought after in the labels
    # and the values are the attribute names in full
    attr_dict = {}
    for line in des:
        if(line[0]=='*'):
            continue
        cline = line.rsplit()
        fname = cline[0]
        psunames = cline[1:]
        for pname in psunames:
            if not(pname == '/'):
                attr_dict[pname] = fname
    return attr_dict

def main():
    # get a dictionary of attributes and their psuedonyms
    attr_dict = get_attr_dict(sys.argv[1])
    print(attr_dict)
    # get all directories of clothing
    dirs = [x for x in os.listdir('./../') if os.path.isdir(x) and not('macys' in x)]
    make_attr_map(dirs,attr_dict)



main()