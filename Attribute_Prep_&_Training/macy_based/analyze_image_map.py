# plot the first 9 images in df
from matplotlib import pyplot
from matplotlib.image import imread
import json, sys

jsf = open(sys.argv[1])
attr_imgs = json.load(jsf)

# plot first few images
i = 0
while i < len(attr_imgs):
    # define filename
    filename = attr_imgs[i][0]
    # load image pixels
    image = imread(filename)

    # print attributes
    print(attr_imgs[i])

    # plot raw pixel data
    pyplot.imshow(image)
    pyplot.show()
    i+=1

# show the figure
pyplot.show()