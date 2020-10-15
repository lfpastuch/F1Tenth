#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 16:14:52 2020

@author: yohas
"""

import rospy
from sensor_msgs.msg import LaserScan


def corrigeGap(lista, valorMin, x=3):
    """
    Entradas é a lista e o valorMinimo 
    Retorna a lista transformando todos os valores menores do que o valor minimo em 0
    Ordem de grandeza máximo 8n -> O(n)
    """
    newlista= []
    for c in range(len(lista)):
        if lista[c] <= valorMin:
            newlista.append(c)
    for n in newlista:
        for i in range(7):
            a=(n + x - i)
            if   a >= 0 and a < len(lista):
                lista[a] = 0
                
    #print str(lista) #print para testes
    return lista

def callback(msg):
    t=len(msg.ranges)
    minDist=3.0
    tempList=[round(msg.ranges[i], 3) for i in range(t) if (i>rangeMin and i<rangeMax)] #transformar a tupple de valores de msgs.ranges
    rospy.loginfo ("O numero de valores lidos são" + str(t))
    #dist = corrigeGap(tempList, minDist)
    dist=tempList
    rospy.loginfo(str(dist))
    
    
rospy.init_node("scan_values")
rangeMax=int(260*1080/360)
rangeMin=int(100*1080/360)
sub = rospy.Subscriber('/scan', LaserScan, callback)
rate=rospy.Rate(10)
rate.sleep()