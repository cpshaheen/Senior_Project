II. Bounding Box
- This directory (and its subdirectories) contains the code for the creation of
bounding box annotations.

Part A: using Body-Pix semantic segmentation

NodeJS v12.16.3

tfjs-models/body-pix/bp-bb/package.json contains the required node packages

First, navigate through the directories to bp-bb:	
	cd tfjs-models/body-pix/bp-bb

Next, install the proper node modules by running:
	npm install

Run the segmentation to get a json file containing pixel arrays of images using:
	node bp_single.js ./path/to/image
	(or bp_dir.js ./path/to/directory/ 
	to iterate over a set of images in a directory)

Part B: processing segmented pixel arrays

Python version 3.8.3

Package                Version
---------------------- ---------
matplotlib             3.2.2
numpy                  1.18.5
Pillow                 7.1.2

After obtaining the json files of pixel arrays, use one of the following python
scripts to produce the required annotation files:

	For tops like shirts and jackets:
		python AnnotateTopDir.py ./path/to/directory/ [optional -v flag 
			for visualizing boxes]
		python AnnotateTop.py ./path/to/image ./path/to/json_of_image 

	For bottoms like pants and shorts:
		python AnnotateBottomDir.py ./path/to/directory/ [optional -v 
			flag for visualizing boxes]
		
	*note: 	when running the python scripts for directories of clothing 
		items, make sure the dictionary at the top of the python script
		reflects the set of categories that will be used
		
	