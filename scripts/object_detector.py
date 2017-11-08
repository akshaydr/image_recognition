#!/usr/bin/env python

import pyyolo
import numpy as np
import sys
import cv2

import rospy
from std_srvs.srv import *
from sensor_msgs.msg import Image

image = None

def handle_request(req):
    print ("Recieved",req)
    return SetBoolResponse(True, 'success')

def image_handler(img_msg):
    global image
     #### direct conversion to CV2 ####
    np_arr = np.fromstring(img_msg.data, np.uint8)
    image = np.reshape(np_arr, (img_msg.height, img_msg.width, 3))
    #cv2.imshow('cv_img', image_np)
    #cv2.waitKey(2)

if __name__ == "__main__":
    rospy.init_node('server')
    s = rospy.Service('my_service', SetBool, handle_request)
    rospy.Subscriber('/camera/image_raw', Image, image_handler)
    print "Ready to recieve."
    rospy.spin()
