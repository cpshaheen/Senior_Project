import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import sys
import os
import statistics
import math

classvals = {
    "tshirts" : 0,
    "jackets" : 1,
    "hoodies": 2,
    "blazer": 7,
    "coat": 8,
    "longsleeve_buttonup": 9,
    "polo": 10,
    "shortsleeve_buttonup": 11,
    "sport_coat": 12,
    "suit_jacket": 13,
    "sweater": 14,
    "sweatshirt": 15,
    "longsleeve_tshirt": 18

}

def topBoundingBox(data,h,w):
    #this function will get the highest and lowest torso y value 
    #and the left most and right most x value determined by either torso or arm
    #note higher y values mean a lower postition
    armvals = [2,3,4,5,6,7,8,9]
    leftx=None
    rightx=None
    topy=None
    bottomy=None
    pixels = data['data']
    i = 0
    while(i < h):
        j = 0
        while(j < w):
            index = (i*w) + j
            pixel = pixels[str(index)]
            if(pixel==12 or pixel==13):
                #torso pixel
                if(leftx == None or leftx>j):
                    leftx = j
                if(rightx == None or rightx<j):
                    rightx = j
                if(topy == None or topy>i):
                    topy = i
                if(bottomy == None or bottomy<i):
                    bottomy = i
            elif(pixel in armvals):
                #arm pixel
                if(leftx == None or leftx>j):
                    leftx = j
                if(rightx == None or rightx<j):
                    rightx = j
            j+=1
        i+=1
    return (leftx,topy),(rightx,bottomy)
    
def procPixels(path):
    #returns a tuple (3 values)
    #the array of pixels, the height and width of the image
    with open(path) as json_file:
        data = json.load(json_file)
        pixels = data['data']
        h = data['height']
        w = data['width']
        return data,h,w

def getRectSize(top_left,bottom_right):
    #returns the width and height (in that order) of the rectangle
    return (bottom_right[0] - top_left[0]),(bottom_right[1] - top_left[1])

def getCenter(top_left,bottom_right):
    centerX = statistics.mean([bottom_right[1],top_left[1]])
    centerY = statistics.mean([bottom_right[0],top_left[0]])
    return (centerX,centerY)

def drawbox(og_image,top_left,bottom_right):
    #get the center position
    center = getCenter(top_left,bottom_right)

    #code from stackoverflow
    im = np.array(Image.open(og_image), dtype=np.uint8)

    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)

    start_pixel = top_left
    rect_size = getRectSize(top_left,bottom_right)

    # Create a Rectangle patch
    rect = patches.Rectangle(top_left,rect_size[0],rect_size[1],linewidth=1,edgecolor='r',facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    #Create a dot patch detailing the center of the object
    dot =  patches.Circle((center[1],center[0]), radius=5, color='red')
    
    #Add patch to Axes
    ax.add_patch(dot)

    plt.show()

def createAnnotation(top_left,bottom_right,abs_w,abs_h,og_path,class_num):
    center = getCenter(top_left,bottom_right)
    bb_dim = getRectSize(top_left,bottom_right) #bounding box dimensions
    '''the format for the annotation file is as follows
        'class# adjCenterX adjCenterY adjWidth adjHeight'
        where adj indicates adjusted relative to the image
        ie: adjCenterX = centerX/absolute width
    '''
    #class_num = 0 #for development only TODO change when classifiying later
    adjCenterX = float(center[0])/float(abs_w)
    adjCenterY = float(center[1])/float(abs_h)
    adjWidth = float(bb_dim[0])/float(abs_w)
    adjHeight = float(bb_dim[1])/float(abs_h)

    # print(f"n{class_num:.4f}\t{adjCenterX:.4f}\t{adjCenterY:.4f}\t{adjWidth:.4f}\t{adjHeight:.4f}\n")
    
    new_path = og_path[:og_path.index(".jpg")]+".txt"
    with open(new_path,"w+") as annotation_file:
        annotation_file.write(f"{class_num} {adjCenterX:.6f} {adjCenterY:.6f} {adjWidth:.6f} {adjHeight:.6f}")
        annotation_file.close()
    

def bounding_box_check(tl,br,w,h,picname):
    # this is a refined test to make sure bounding boxes are reasonable
    # first we test to see if the width of the box is less than the height
    # next we test if the center of the box is within the center third of the image
    center_third = float(w)/float(3)
    box_center = getCenter(tl,br)[1]
    box_width, box_height = getRectSize(tl,br)
    epsilon = math.sqrt(statistics.mean([w,h]))

    # print(f"box_center = {box_center}, first center_third = {center_third}, second center_third = {2*center_third}")
    # print(f"box_width = {box_width}, box_height = {box_height}")

    if (((box_width - box_height) < epsilon) and (box_center>center_third and box_center<(2*center_third))):
        return True
    else:
        return False

def main():
    i = 0
    if(len(sys.argv)==1):
        print(f"USAGE: {__file__} [clothing tops directory]\n\toptional flag: [-v or -visual] for viewing bounding boxes")
        exit()
    clothingType = sys.argv[1].split('/')
    clothingType = clothingType[len(clothingType)-2]
    classnum = classvals[clothingType]
    visual = False
    if(len(sys.argv)>=3 and (sys.argv[2]=='-v' or sys.argv[2]=='-visual')):
        visual = True
    names = [sys.argv[1]+f[:f.index(".jpg")] for f in os.listdir(sys.argv[1]) if ".jpg" in f]
    for name in names:
        i+=1
        pct = int(100 * i/len(names))
        print(f"\t%{pct} complete", end='\r', flush=True) 
        imgname = name+".jpg"
        jsonname = name+"_sgmt.json"
        txtname = name+".txt"
        if(os.path.isfile(jsonname) and not(os.path.isfile(txtname))):
            d,h,w = procPixels(jsonname)
            top_left,bottom_right = topBoundingBox(d,h,w)
            if not(None in top_left or None in bottom_right) and (bounding_box_check(top_left,bottom_right,w,h,imgname)):
                createAnnotation(top_left,bottom_right,w,h,imgname,classnum)
                # for visual testing/debugging purposes only
                if(visual):
                    drawbox(imgname,top_left,bottom_right)
            else:
                # in this case the wasnt properly segmented so
                # we will remove the json and jpeg files
                os.remove(imgname)
                os.remove(jsonname)
                

main()
