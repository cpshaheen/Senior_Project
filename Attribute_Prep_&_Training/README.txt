IV. Attribute Preparation + Training
- This directory contains the code for attribute predictions preparation and 
  training.
- There are two versions, one which uses the DeepFashion dataset, and another 
  that uses the web scraped clothing from macys. The code for training and
  testing is nearly identical other than the input image dimensions of the
  model and the creation of the image and attribute mapping.

Part A: data preparation
- To use the Macy's preparation files move the clothing_classes
  directory to the macys_based folder
- To use the DeepFashion preparation files please download and unzip the 
  dataset from the following link: 
	https://drive.google.com/open?id=0B7EVK8r0v71pQ2FuZ0k0QnhBQnc

Python version 3.6.10

Package                Version
---------------------- ---------
numpy                  1.18.5             
matplotlib             3.2.2
Keras                  2.4.3              
Keras-Applications     1.0.8              
Keras-Preprocessing    1.1.2   
pandas                 1.0.5              

First, make sure that the data is in the same directory as df_attr_prep.py 
(or macys_attr_prep.py for the macys images version). 
    - For the DeepFashion version, provide a text file of desired attributes
      from the list in the DeepFashion Anno directory in the same format as the 
      provided example desired_attrs_df.txt. 
    - For the macys version, provide a similar txt file in the format of the
      provided example desired_attrs_macys.txt
        - note that this format on each line is:
            desired_attribte / attribute_keyword_1 / attribute_keyword_2 ...

Then, run df_attr_prep.py with the attribute list text file provided as an
argument. This will output a json file that contains mapping of images to their
attributes.

Use analyze_image_map.py with the newly created json file to make sure that the 
attributes correspond to the images properly.

Once the images have been analyzed, run map_lbl_imgs.py with the previously
mentioned json file as the first argument. this will output three json files. 
    - attrs_map.json: contains a mapping of attributes to their one hot
      encoded index position
    - inv_attrs_map.json: an inverse of the above mapping.
    - imgs_attrs_map.json: a mapping of image paths and their one hot encoding
      of attributes for training

With attrs_map.json and imgs_attrs_map.json we can package the data for 
training. Run make_dataset.py to create deepfashion_data.npz (macys_data.npz 
for the macys data) 
    - make sure to include attrs_map.json file as the first argument and 
      imgs_attrs_map.json as the second argument with the optional '-s' flag 
      at the end of the command followed by the desired max set size to limit
      the size of the data.

Part B: model design and training:
- Training is nearly identical in both cases so the following instructions will 
  work in either case.

Python version 3.6.8

Package                Version
---------------------- ---------
Keras                  2.3.0
Keras-Applications     1.0.8
Keras-Preprocessing    1.1.2
matplotlib             3.2.2
numpy                  1.19.0
pandas                 1.0.5
sklearn                0.0
scikit-learn           0.23.1
scipy                  1.4.1

With the .npz data in the current working directory, train the model by passing 
the data as the first argument to train.py. This will output a .png file that 
contains the training evaluation and a .h5 file that will contain the model.

After training is complete the model can be evaluated on an image using test.py.
To use test.py, provide the following arguments in the order they appear:
	- the model (.h5 file)
	- the inverse mapping
	- the image to be evaluated
