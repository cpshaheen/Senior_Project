import sys, json
from datetime import date

today = date.today()
# this script takes the list of given attributes provided 
# as the first cli argument and finds images that contain at least one
# of those attributes. it also merges similar attributes to limit
# the number of classes for simplicity sake

# animal_labels = ['animal','bird','butterfly','cheetah','dolphin','giraffe','leopard']
camo_labels = ['camo','camouflage']
dot_labels = ['dot']
leather_labels = ['leather']
hood_labels = ['hood']
zip_labels = ['zip']
button_labels = ['button']
plaid_labels = ['plaid', 'tartan']
fur_labels = ['fur']
denim_labels = ['denim','jean']

title_labels = ['plaid', 'jean', 'button','leather','hood','camo','denim','zip','fur']

def merge_label(label):
    # merge shared label attributes
    # if any(alabel in label for alabel in animal_labels):
    #     return 'animal_print'
    if any(clabel in label for clabel in camo_labels):
        return 'camouflage'

    if any(dlabel in label for dlabel in dot_labels):
        return 'dotted'

    if any(blabel in label for blabel in button_labels):
        return 'buttoned'
    
    if any(flabel in label for flabel in fur_labels):
        return 'fur'

    if any(llabel in label for llabel in leather_labels):
        return 'leather'
    
    if any(hlabel in label for hlabel in hood_labels):
        return 'hooded'

    if any(zlabel in label for zlabel in zip_labels):
        return 'zipped'

    if any(plabel in label for plabel in plaid_labels):
        return 'plaid'
    
    if any(dlabel  in label for dlabel in denim_labels):
        return 'denim'

    return label

def title_label_merge(cur_img,des_attrs):
    # function takes array with img_name and the list of img labels
    # checks to see if the title contains labels that were not 
    # already in the list of labels provided by deepfashion
    for label in title_labels:
        if(label in cur_img[0].lower() and not(merge_label(label) in cur_img[1])):
            cur_img[1].append(merge_label(label))
    return cur_img

def make_json(img_list, des_attr_dict):
    attr_imgs = []
    # going through images
    i = 0
    for img in img_list:
        print(f" {((i/len(img_list))*100):.2f} % complete", sep=' ', end='\r', flush=True)
        i+=1
        img_name = img.split()[0]
        # skip over dresses and blouses 
        # if 'dress' in img_name.lower() or 'blouse' in img_name.lower():
        #     continue 
        img_attrs = img.split()[1:]
        # going through image attributes
        cur_img = [img_name,[]]
        for idx in des_attr_dict.keys():
            if img_attrs[idx] == '1':
                # check if this label is in the list already
                # and append the list if not
                nlabel = merge_label(des_attr_dict[idx])
                if not(nlabel in cur_img[1]):
                    cur_img[1].append(nlabel)
        # check if the title contains a label that is not already in the 
        # list of labels 
        # cur_img = title_label_merge(cur_img,des_attr_dict.values())
        if not(cur_img in attr_imgs) and (len(cur_img[1])>0):
            attr_imgs.append(cur_img)
    
    # saving the images and their attributes to a json file
    f = open('img_attrs_'+ today.strftime("%m-%d-%y") +'.json', 'w')
    print(len(attr_imgs))
    json.dump(attr_imgs, f)
    f.close()

def main():
    # read in the desired list of attribute
    f = open(sys.argv[1], 'r')
    des = f.readlines()[2:]
    f.close()

    for i in range(len(des)):
        des[i] = des[i].rstrip()[:-1].rstrip()

    # read in the list of attributes
    f = open('./Anno/list_attr_cloth.txt', 'r')
    attrs = f.readlines()[2:]
    f.close()

    for i in range(len(attrs)):
        attrs[i] = attrs[i].rstrip()[:-1].rstrip()

    # make a list of tuples of attributes and their index value
    des_attr_dict = {}

    for idx, val in enumerate(attrs):
        if val in des:
            des_attr_dict[idx-2] =  val

    print(des_attr_dict)

    # iterate through the images and see if it contains a desired attribute
    f = open('./Anno/list_attr_img.txt', 'r')
    img_list = f.readlines()[2:]
    f.close()

    make_json(img_list,des_attr_dict)

main()