#!/usr/bin/env python

import pyyolo
import numpy as np
import sys
import cv2

import rospy
from std_srvs.srv import *
from sensor_msgs.msg import Image

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

darknet_path = dir_path + '/../pyyolo/darknet'
datacfg = dir_path + '/../pyyolo/darknet/cfg/coco.data'
cfgfile = dir_path + '/../pyyolo/darknet/cfg/tiny-yolo.cfg'
weightfile = dir_path + '/../pyyolo/tiny-yolo.weights'

image = None

def detect():
    global image

    img = image.transpose(2,0,1)
    c, h, w = img.shape[0], img.shape[1], img.shape[2]

    data = img.ravel()/255.0
    data = np.ascontiguousarray(data, dtype=np.float32)
    outputs = pyyolo.detect(w, h, c, data, 0.24, 0.5) #thresh, heir_thresh

    return outputs

def handle_request(req):
    print ("Recieved",req)
    r = detect()
    if(len(r) == 0):
        return SetBoolResponse(False, str(r))
    else:
        return SetBoolResponse(True, str(r))

def image_handler(img_msg):
    global image
     #### direct conversion to CV2 ####
    np_arr = np.fromstring(img_msg.data, np.uint8)
    image = np.reshape(np_arr, (img_msg.height, img_msg.width, 3))
    #cv2.imshow('cv_img', image_np)
    #cv2.waitKey(2)

if __name__ == "__main__":
    rospy.init_node('server')
    s = rospy.Service('detect', SetBool, handle_request)
    rospy.Subscriber('/camera/image_raw', Image, image_handler)

    pyyolo.init(darknet_path, datacfg, cfgfile, weightfile)

    print "Ready to recieve."
    rospy.spin()

    pyyolo.cleanup()
    print("Done Cleaning...")
