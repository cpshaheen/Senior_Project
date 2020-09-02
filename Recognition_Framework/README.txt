V. Framework 
- This directory contains the code required for using the models from
  previous portions to analyze a video feed (either live feed or 
  pre-recorded)
- There are two main parts: the first deals with converting the YOLOv4 model
  to a tensorflow model so that it can be used with python and opencv for 
  analysis. The next part deals with running the program.
- Both portions rely on the following GitHub repo, so please clone it:
	https://github.com/hunglc007/tensorflow-yolov4-tflite
- Replace detectvideo.py in the GitHub repository with the version in the
  current directory. Also replace utils.py inside of the repository's core
  directory with the version in the current directory. 
- Place the .names file inside of the repositories ./data/classes directory

Part A: model conversion
- Make sure the above GitHub repository is cloned. Move the YOLO weights
  and the .names file into the repository directory.

Python version 3.6.10

Package                Version            
---------------------- -------------------
tensorflow             2.3.0rc0           

To covert a YOLOv4 model to be used with tensorflow in python run
save_model.py. Refer to to the GitHub README for details on how to run it.

Part B: analyzing video feed
- Again, make sure the above GitHub repository is cloned. Move the attribute 
  prediction model and the inverse mapping into the repository directory.
- Again, make sure to replace detectvideo.py in the GitHub repository with 
  the version in the current directory. Also replace utils.py inside of the 
  repository's core directory with the version in the current directory. 
- Depending on if the video feed is live from a device or from a prerecorded
  video, their maybe compatibility issues with the frame aspect ratios and
  the video encoding. Currently it's written to accept .mp4 videos. There
  is an included script (getframesrotate.py) that I used for encoding
  conversion and orientation. It is a good reference on how to make a similar
  script for a different compatibility issue.

Python version 3.6.10

Package                Version
---------------------- ---------
numpy                  1.18.5             
matplotlib             3.2.2
Keras                  2.4.3              
Keras-Applications     1.0.8              
Keras-Preprocessing    1.1.2   
pandas                 1.0.5   
tensorflow             2.3.0rc0           


To run, look at the following example run. More options and features are
available from the original detectvideo.py, however it is unclear if the 
additional features will result in issues with the modified version.

The flag --weights is for the yolov4 converted weights, the flag --model
refers to the version of yolo (either v3 or v4, we use v4 in this case),
the --attr_model flag is for the attribute prediction model, the --inv_map
flag is for inverse mapping of the attributes, and lastly the --video flag
specifies the path to the video footage to be analyzed.     

Example run:
	
python detectvideo.py --weights ./checkpoints/yolov4-clth --size 416 
--model yolov4 --attr_model ./attr_cfg/final_model_07-23-20.h5 --inv_map 
./attr_cfg/inv_attrs_map_07-22-20.json --video ./../test_clips/sportcoat_R.mp4 

Some test clips have been provided. In addition to those, the models used above 
have also been provided. Since the size of these models is larger than the GitHub
file maximum, they will be accessible from the following google drive link:
	- link for attribute model (deepfashion): https://drive.google.com/file/d/1VNegNbbgfRscvpA9SiHBLXqLv1kBP7tT/view?usp=sharing
	- link for converted yolov4 model: https://drive.google.com/file/d/1mtsd9CZCI3pHvlA18nfQYK2KPTYAZ4TE/view?usp=sharing
