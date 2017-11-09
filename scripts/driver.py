#!/usr/bin/env python

RPI = False

import rospy
from std_msgs.msg import Int32

if RPI:
import RPi.GPIO as

# PWM pins are 12, 13, 18, 19, 40

if RPI:
    GPIO.setmode(GPIO.BOARD)

    M1pwm = 12
    M1dir = 3   #Motor 1

    M2pwm = 13
    M2dir = 5   #Motor 2

    M3pwm = 18
    M3dir = 7   #Motor 3

    M4pwm = 19
    M4dir = 16  #Motor 4

    GPIO.setup(relay, GPIO.OUT)
    GPIO.setup(M1pwm, GPIO.OUT)
    GPIO.setup(M1dir, GPIO.OUT)
    GPIO.setup(M2pwm, GPIO.OUT)
    GPIO.setup(M2dir, GPIO.OUT)
    GPIO.setup(M3pwm, GPIO.OUT)
    GPIO.setup(M3dir, GPIO.OUT)
    GPIO.setup(M4pwm, GPIO.OUT)
    GPIO.setup(M4dir, GPIO.OUT)

    GPIO.output(M1pwm, GPIO.LOW)
    GPIO.output(M1dir, GPIO.LOW)
    GPIO.output(M2pwm, GPIO.LOW)
    GPIO.output(M2dir, GPIO.LOW)
    GPIO.output(M3pwm, GPIO.LOW)
    GPIO.output(M3dir, GPIO.LOW)
    GPIO.output(M4pwm, GPIO.LOW)
    GPIO.output(M4dir, GPIO.LOW)

    pwm1 = GPIO.PWM(M1pwm, 90)
    pwm2 = GPIO.PWM(M2pwm, 90)
    pwm3 = GPIO.PWM(M3pwm, 90)
    pwm4 = GPIO.PWM(M4pwm, 90)
else :
    print("Simulated setup done!")

def callback(msg):
    if (msg.data > 320):
        pwm1.start(50)
        pwm2.start(50)
        pwm3.start(50)
        pwm4.start(50)
        GPIO.output(M1dir, GPIO.HIGH)
        GPIO.output(M2dir, GPIO.HIGH)
        GPIO.output(M3dir, GPIO.LOW)
        GPIO.output(M4dir, GPIO.LOW)
        sleep(0.8)
        # Move bot left by 15 degree
    if (msg.data < 320):
        pwm1.start(50)
        pwm2.start(50)
        pwm3.start(50)
        pwm4.start(50)
        GPIO.output(M1dir, GPIO.LOW)
        GPIO.output(M2dir, GPIO.LOW)
        GPIO.output(M3dir, GPIO.HIGH)
        GPIO.output(M4dir, GPIO.HIGH)
        sleep(0.8)
        # Move bot right by 15 degree

if __name__ == '__main__':
  rospy.init_node('driver')
  rospy.Subscriber('driver', Int32, callback)

  while not rospy.is_shutdown():
    rospy.spin()
