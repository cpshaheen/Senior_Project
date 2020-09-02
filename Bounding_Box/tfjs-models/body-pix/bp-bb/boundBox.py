import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import sys

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

def drawbox(og_image,top_left,bottom_right):
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

    plt.show()

def main():
    if(sys.argv[1]==None or sys.argv[2]==None):
        print(f"USAGE: {__file__} [original image] [segmetation json file]")
        exit()
    d,h,w = procPixels(sys.argv[2])
    top_left,bottom_right = topBoundingBox(d,h,w)
    drawbox(sys.argv[1],top_left,bottom_right)

main()