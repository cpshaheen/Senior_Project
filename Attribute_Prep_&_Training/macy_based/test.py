# make a prediction for a new image

# TO USE:
# provide the model as the first argument,
# provide the inverse mapping as the second argument
# provide the image as the last argument

import sys, json
from pandas import read_csv
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import backend

# create a mapping of tags to integers given the loaded mapping file
def create_tag_mapping(mapping_csv):
        # create a set of all known tags
        labels = set()
        for i in range(len(mapping_csv)):
                # convert spaced separated tags into an array of tags
                tags = mapping_csv['tags'][i].split(' ')
                # add tags to the set of known labels
                labels.update(tags)
        # convert set of labels to a list to list
        labels = list(labels)
        # order set alphabetically
        labels.sort()
        # dict that maps labels to integers, and the reverse
        labels_map = {labels[i]:i for i in range(len(labels))}
        inv_labels_map = {i:labels[i] for i in range(len(labels))}
        return labels_map, inv_labels_map

# convert a prediction to tags
def prediction_to_tags(inv_mapping, prediction):
        # round probabilities to {0, 1}
        print(prediction)
        values = prediction.round()
        # collect all predicted tags
        tags = [inv_mapping[str(i)] for i in range(len(values)) if values[i] == 1.0]
        return tags

# load and prepare the image
def load_image(filename):
        # load the image
        img = load_img(filename, target_size=(320, 400))
        # convert to array
        img = img_to_array(img)
        # reshape into a single sample with 3 channels
        img = img.reshape(1, 320, 400, 3)
        # center pixel data
        img = img.astype('float32')
        img = img - [123.68, 116.779, 103.939]
        return img

# calculate fbeta score for multi-class/label classification
def fbeta(y_true, y_pred, beta=2):
    # clip predictions
    y_pred = backend.clip(y_pred, 0, 1)
    # calculate elements
    tp = backend.sum(backend.round(backend.clip(y_true * y_pred, 0, 1)), axis=1)
    fp = backend.sum(backend.round(backend.clip(y_pred - y_true, 0, 1)), axis=1)
    fn = backend.sum(backend.round(backend.clip(y_true - y_pred, 0, 1)), axis=1)
    # calculate precision
    p = tp / (tp + fp + backend.epsilon())
    # calculate recall
    r = tp / (tp + fn + backend.epsilon())
    # calculate fbeta, averaged across each class
    bb = beta ** 2
    fbeta_score = backend.mean((1 + bb) * (p * r) / (bb * p + r + backend.epsilon()))
    return fbeta_score

# load an image and predict the class
def run_example():
        # load the inv mapping
        im_file = open(sys.argv[2],'r')
        inv_mapping = json.load(im_file)
        print(inv_mapping)
        # load the image
        img = load_image(sys.argv[3])
        # load model
        model = load_model(sys.argv[1], custom_objects={"fbeta":fbeta})
        # predict the class
        result = model.predict(img)
        print(result[0])
        # map prediction to tags
        tags = prediction_to_tags(inv_mapping, result[0])
        print(tags)

# entry point, run the example
run_example()