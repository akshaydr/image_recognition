#!/usr/bin/env python

import sys
import rospy
import cv2
import numpy as np
from std_srvs.srv import *
from sensor_msgs.msg import Image
import ast
from std_msgs.msg import Int32

bounds = None
image = None

mousex = 0
mousey = 0
obj_dist = 0

def mousePosition(event,x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE:
        print x,y

def draw(img_msg):
    global image, mousey, mousex
    #### direct conversion to CV2 ####
    np_arr = np.fromstring(img_msg.data, np.uint8)
    image = np.reshape(np_arr, (img_msg.height, img_msg.width, 3))
    if(bounds != None):
        for output in bounds:
            cv2.putText(image, output['class'],(output['left'], output['top']), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255,255,255),2)
            cv2.rectangle(image,(output['left'], output['top']), (output['right'], output['bottom']),(0,255,0),3)
            if (mousex > output['left'] and mousex < output['right'] and mousey > output['top'] and mousey < output['bottom']):
                print ("Selected", output['class'])
                obj_dist = output['left'] + output['right'])/2
                pub.publish(obj_dist)
            # x = (output['left'] + output['right']) /2
            # y = (output['top'] + output['bottom']) /2
            # cv2.circle(image,(x, y), 4, (0,255,0), -1)

def callDetector():
    global bounds
    try:
        detect = rospy.ServiceProxy('detect', SetBool)
        resp1 = detect(True)
        bounds = ast.literal_eval(resp1.message)

    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def on_mouse(event, x, y, flags, params):
    global mousex, mousey
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mousex = x
        mousey = y

if __name__ == "__main__":
    global mousey, mousex
    rospy.init_node('Receiver')
    rospy.wait_for_service('detect')

    rospy.Subscriber('/camera/image_raw', Image, draw)
    pub = rospy.Publisher('driver', Int32, queue_size=10)
    # callDetector()

    while not rospy.is_shutdown():
        if not image == None:
            cv2.namedWindow('real image')
            cv2.setMouseCallback('real image',on_mouse)
            cv2.imshow('real image', image)
        #     cv2.imshow('cv_img', image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        if key == ord('r'):
            callDetector()
            mousex = 0
            mousey = 0


    cv2.destroyAllWindows()
