import json, sys
from datetime import date

today = date.today()
# this script creates a mapping (and inverse mapping) of
# all attributes in the image list for future 1 hot encoding
# also converts the img_attrs.json file to a mapping of files
# to their labels

# provide img_attrs.json (the map of mapping of files and images) 
# as the first arg. comes from df_attr_prep.py

jsf = open(sys.argv[1])
attr_imgs = json.load(jsf)
jsf.close()

# creating a dictionary that maps each label to a index for 1 hot enc
# and converting the img_attrs.json file to a mapping of filenames
# to their labels
img_attr_dict = {}
labels_dict = {}

for img in attr_imgs:
    img_attr_dict[img[0]] = img[1]
    for label in img[1]:
        if not(label in labels_dict.keys()):
            labels_dict[label] = len(labels_dict)

print(labels_dict)
print(img_attr_dict, len(img_attr_dict))

# saving the images attributes to a json file
f = open('attrs_map_'+ today.strftime("%m-%d-%y") +'.json', 'w')
json.dump(labels_dict, f)
f.close()

# saving the images and their attributes map to a json
f = open('imgs_attrs_map_'+ today.strftime("%m-%d-%y") +'.json', 'w')
json.dump(img_attr_dict, f)
f.close()

# creating the inverse mapping of the label for prediction translation
inv_labels_dict = {}

for key in labels_dict.keys():
    inv_labels_dict[labels_dict[key]] = key

print(inv_labels_dict)

# saving inverse mapping to a json file
f = open('inv_attrs_map_'+ today.strftime("%m-%d-%y") +'.json', 'w')
json.dump(inv_labels_dict, f)
f.close()