III. YOLOv4 Data Preparation + Training
- This directory contains the code for the creation of the data splits
  (split_data.py).
- It also contains example configuration files that were used for training
  (ex_cfg_files).

Part A: getting YOLOv4 

First, clone the following YOLOv4 repository and navigate inside of it: 
	https://github.com/AlexeyAB/darknet

*note: refer to the readme of the GitHub repo for 
more information on the frame work and configuration.

Next, configure the Makefile to take advantage of your machines gpu, 
libraries, etc. and compile the darknet framework. (Refer to the repo README)

Then, create a directory inside the darknet directory to hold the clothing items 
and the configuration files (we will refer to this directory as clth_stuff). And
move the outer directory that holds all the clothing categories into clth_stuff 
(the newly created directory).

Part B: splitting data 

Python version 3.8.3

No packages required

First, make sure the bounding box annotations were made for all categories.

Next, navigate to clth_stuff and run split_data.py to create test.txt and 
train.txt by specifying the directory that holds the various clothing 
category's' folders:
	python split_data.py ./path/to/clth_ctgs


Now a set of test and train text files will be in the directory. You can remove
all but test.txt and train.txt. running the following command should do the 
trick:
	rm *_.txt

Part C: training and configuration

The provided .cfg file inside of ex_cfg_files has been modified for the number
of clothing. Copy this file along with the .names file to clth_stuff. 
Modify the .data file to properly reflect the locations of the file paths and
then copy the newly modified file to the clth_stuff directory.

Next, download the following pre-trained set of weights into clth_stuff: 
	https://github.com/AlexeyAB/darknet/releases/download/
	darknet_yolo_v3_optimal/yolov4.conv.137

Now begin training by running the following command:
	./darknet detector train path/to/.data path/to/.cfg path/to/
	yolov4.conv.137

*note: training may take very long - up to a number of days. If training time is
unviable, start over and use a smaller set of categories. 

