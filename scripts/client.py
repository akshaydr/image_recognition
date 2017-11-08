#!/usr/bin/env python

import sys
import rospy
from std_srvs.srv import *

def add_two_ints_client(data):
    rospy.wait_for_service('my_service')
    try:
        my_service = rospy.ServiceProxy('my_service', SetBool)
        resp1 = my_service(data)
        return resp1.success, resp1.message
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    data = True
    print ("Requesting",data)
    print (add_two_ints_client(data))
