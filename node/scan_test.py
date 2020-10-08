#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 16:14:52 2020

@author: yohas
"""

import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
    t=len(msg.ranges)
    rospy.loginfo ("O numero de valores lidos são" + str(t))

rospy.init_node("scan_values")
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()