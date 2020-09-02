import time
import ast
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from core.config import cfg

import sys, json
from pandas import read_csv
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import backend

flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('video', './data/road.mp4', 'path to input video')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.25, 'score threshold')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
flags.DEFINE_string('attr_model',None, 'the keras model responsible for attribute prediction')
flags.DEFINE_string('inv_map',None, 'the mapping of keras predictions for the one hot encoding to the attr names')
flags.DEFINE_boolean('dis_cv2_window', False, 'disable cv2 window during the process') # this is good for the .ipynb

# convert a prediction to tags
def prediction_to_tags(inv_mapping, prediction):
    # round probabilities to {0, 1}
    values = prediction.round()
    # collect all predicted tags
    tags = [inv_mapping[str(i)] for i in range(len(values)) if values[i] == 1.0]
    return tags

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

def attr_pred(crop_img, attr_model, inv_mapping):
    # make prediction about the attributes of the detected clothing item
    crop_img = cv2.resize(crop_img, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)
    # cv2.imshow("crop_img_attr_pred", crop_img)
    crop_img = crop_img.reshape(1, 256, 256, 3)
    crop_img = crop_img.astype('float32')
    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)

    crop_img = crop_img - [123.68, 116.779, 103.939]
    res = attr_model.predict(crop_img)
    tags = prediction_to_tags(inv_mapping, res[0])
    # print(tags)
    return tags

def object_sifter(frame_anlys):
    # func will return the obj detection that is the most prevalent in all frames
    count_dict = {}
    for i, f in enumerate(frame_anlys):
        cloth_objs = set() #empty set
        for c in f:
            cloth_objs.add(c[0].split()[0][:-1])
        cloth_objs = sorted(cloth_objs)

        if count_dict.get(str(cloth_objs))!=None:
            count_dict[str(cloth_objs)][0] = count_dict[str(cloth_objs)][0] + 1
            count_dict[str(cloth_objs)][1].append(i)
        else:
            count_dict[str(cloth_objs)] = [1,[]]

    print(count_dict)
    if count_dict.get('[]')!=None:
        count_dict.pop('[]')
    rec_cloths = max(count_dict, key=count_dict.get)
    print(rec_cloths)
    cloths_idxs = count_dict[rec_cloths][1]

    return rec_cloths, cloths_idxs

def box_sifter(box_preds, clothing_predictions, clothing_items):
    # func will return the boxes that have the set of clothing at the highest prediction confidence
    # print(box_preds[0])
    # print(clothing_predictions[0])
    # print(clothing_items[0]) # ex: 'tshirt'

    # list of dictionaries that are responisble for keeping track of the max prediction value for 
    # each clothing item and the boxes of that predictions frame

    max_pred_dicts = {}
    for item in clothing_items:
        max_pred_dicts[item] = (0.0, None)
    # loop over frames that contain clothing objects
    for f, frame in enumerate(clothing_predictions):
        # loop over items in the frame
        for i, item in enumerate(frame):
            item_name = item[0].split()[0][:-1]
            item_prediction = item[0].split()[1]
            if max_pred_dicts[item_name][0] < float(item_prediction):
                max_pred_dicts[item_name] = (float(item_prediction),box_preds[f][i])
    return max_pred_dicts

def attr_sifter(attr_frames, num_clothes):
    # func will return the attribute that was the most 
    # prevalent when that clothing object was present on screen

    # create seperate count dictionaries for each clothing item
    clth_count_dicts = []
    for i in range(num_clothes):
        clth_count_dicts.append({})


    # loop over each frames sets of attributes
    for attr_frame in attr_frames:
        # loop over each clothing item in the set
        for i, clth_item_attrs in enumerate(attr_frame):
            if i > num_clothes-1:
                break
            clth_attrs = set()
            # loop over each attribute of the clothing item
            for attr in clth_item_attrs:
                clth_attrs.add(str(attr))
            clth_attrs = " ".join(sorted(clth_attrs))
            if clth_count_dicts[i].get(str(clth_attrs))!=None:
                 clth_count_dicts[i][str(clth_attrs)] = clth_count_dicts[i][str(clth_attrs)] + 1
            else:
                clth_count_dicts[i][str(clth_attrs)] = 1

    print(clth_count_dicts)
    total_frames = len(attr_frame)

    ret_attr_list = []
    for d in clth_count_dicts:
        rec_attrs = max(d, key=d.get)
        if d[rec_attrs] >= float(total_frames)/10:
            ret_attr_list.append(rec_attrs)
        else:
            ret_attr_list = []
    return ret_attr_list

def frame_sifter(obj_preds,box_preds,attr_preds):
    if not any(obj_preds):
        print("no clothing items recognized")
        sys.exit()


    # func will 'sift' through the returned frames and determine 
    # what the most common predicted set of clothes were along with their attributes 
    clothing_items, items_index = object_sifter(obj_preds)
    clothing_items = ast.literal_eval(clothing_items)

    if len(items_index) == 0:
        print("no clothing items recognized")
        sys.exit()
    num_clth_items = len(obj_preds[items_index[0]])
    clothing_objects = [obj_preds[i] for i in items_index]
    clothing_boxes = [box_preds[i] for i in items_index]
    clothing_attrs = [attr_preds[i] for i in items_index]

    # get the boxes with the highest prediction for each clothing item
    clothing_boxes = box_sifter(clothing_boxes,clothing_objects,clothing_items)

    # func will 'sift' through the frames and their bounding boxes and determine
    # what the best image to use is
    clothing_attrs = attr_sifter(attr_preds, num_clth_items)
    # clothing_attrs = " ".join(clothing_attrs)
    # print(clothing_attrs)
    # print('clothing attrs list length ' + str(len(clothing_attrs)))
    # print('first item in clothing attrs ' + str(len(clothing_attrs[0])))
    # return each clothing item and its attributes
    for i, clth_item in enumerate(clothing_items):
        print('clothing item: ' + clth_item)
        if len(clothing_attrs)>i and clothing_attrs[i]:
            print('attributes: ' + clothing_attrs[i])
        cv2.imshow(clth_item, clothing_boxes[clth_item][1])
        cv2.waitKey(0)


def main(_argv):
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    video_path = FLAGS.video

    print("Video from: ", video_path )
    vid = cv2.VideoCapture(video_path)

    if FLAGS.framework == 'tflite':
        interpreter = tf.lite.Interpreter(model_path=FLAGS.weights)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        print(input_details)
        print(output_details)
    else:
        saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
        infer = saved_model_loaded.signatures['serving_default'] 
    
    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))
    
    # load attr model
    attr_model = load_model(FLAGS.attr_model, custom_objects={"fbeta":fbeta})

    # load the inv_mapping
    im_file = open(FLAGS.inv_map,'r')
    inv_mapping = json.load(im_file)

    # list of clothing types and their corresponding bounding 
    # boxes along with their predicted attribtues
    obj_preds, box_preds, attr_preds = [], [], []

    frame_id = 0
    while True:
        return_value, frame = vid.read()
        ogframe = frame
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
        else:
            if frame_id == vid.get(cv2.CAP_PROP_FRAME_COUNT):
                print("Video processing complete")
                break
            raise ValueError("No image! Try with another video format")
        
        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        prev_time = time.time()

        if FLAGS.framework == 'tflite':
            interpreter.set_tensor(input_details[0]['index'], image_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            if FLAGS.model == 'yolov3' and FLAGS.tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
        else:
            batch_data = tf.constant(image_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )
        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        bbframe = frame.copy()
        frame_boxes, tag_list = utils.get_bbox(frame, pred_bbox, attr_model, inv_mapping)
        item, image = utils.draw_bbox(bbframe, pred_bbox)

        obj_preds.append(item)
        box_preds.append(frame_boxes)
        attr_preds.append(tag_list)
        
        curr_time = time.time()
        exec_time = curr_time - prev_time
        result = np.asarray(image)
        info = "time: %.2f ms" %(1000*exec_time)

        result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if not FLAGS.dis_cv2_window:
            cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("result", result)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        if FLAGS.output:
            result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
            out.write(result)
        
        frame_id += 1

    # print(obj_preds)
    # print(box_preds)
    # print(attr_preds)
    # sys.exit()
    frame_sifter(obj_preds, box_preds, attr_preds)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
