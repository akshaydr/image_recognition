#!/usr/bin/env python

import sys
import rospy
import cv2
import numpy as np
from std_srvs.srv import *
from sensor_msgs.msg import Image
import ast

bounds = None
image = None
def draw(img_msg):
    global image
    #### direct conversion to CV2 ####
    np_arr = np.fromstring(img_msg.data, np.uint8)
    image = np.reshape(np_arr, (img_msg.height, img_msg.width, 3))
    if(bounds != None):
        for output in bounds:
    		cv2.putText(image, output['class'],(output['left'], output['top']), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255,255,255),2)
    		cv2.rectangle(image,(output['left'], output['top']), (output['right'], output['bottom']),(0,255,0),3)
    		x = (output['left'] + output['right']) /2
    		y = (output['top'] + output['bottom']) /2
    		cv2.circle(image,(x, y), 4, (0,255,0), -1)

def callDetector():
    global bounds
    try:
        detect = rospy.ServiceProxy('detect', SetBool)
        resp1 = detect(True)
        bounds = ast.literal_eval(resp1.message)

    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    rospy.init_node('Receiver')
    rospy.wait_for_service('detect')

    rospy.Subscriber('/camera/image_raw', Image, draw)
    # callDetector()

    while not rospy.is_shutdown():
        if not image == None:
            cv2.imshow('cv_img', image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        if key == ord('r'):
            callDetector()

    cv2.destroyAllWindows()
