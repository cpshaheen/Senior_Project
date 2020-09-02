import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import sys
import statistics

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
    #returns the height and width of the rectangle
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

def createAnnotation(top_left,bottom_right,abs_w,abs_h,og_path):
    center = getCenter(top_left,bottom_right)
    bb_dim = getRectSize(top_left,bottom_right) #bounding box dimensions
    '''the format for the annotation file is as follows
        'class# adjCenterX adjCenterY adjWidth adjHeight'
        where adj indicates adjusted relative to the image
        ie: adjCenterX = centerX/absolute width
    '''
    class_num = 0 #for development only TODO change when classifiying later
    adjCenterX = float(center[0])/float(abs_w)
    adjCenterY = float(center[1])/float(abs_h)
    adjWidth = float(bb_dim[0])/float(abs_w)
    adjHeight = float(bb_dim[1])/float(abs_h)

    print(f"Annotation\n{class_num:.4f}\t{adjCenterX:.4f}\t{adjCenterY:.4f}\t{adjWidth:.4f}\t{adjHeight:.4f}\n")
    
    new_path = og_path[:og_path.index(".jpg")]+".txt"
    with open(new_path,"w+") as annotation_file:
        annotation_file.write(f"{class_num} {adjCenterX:.6f} {adjCenterY:.6f} {adjWidth:.6f} {adjHeight:.6f}")
        annotation_file.close()
    

def main():
    if(sys.argv[1]==None or sys.argv[2]==None):
        print(f"USAGE: {__file__} [original image] [segmetation json file]")
        exit()
    d,h,w = procPixels(sys.argv[2])
    top_left,bottom_right = topBoundingBox(d,h,w)
    createAnnotation(top_left,bottom_right,w,h,sys.argv[1])
    drawbox(sys.argv[1],top_left,bottom_right)

main()