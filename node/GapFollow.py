#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 17:39:38 2020

@author: yohas
"""
#Importando as bibliotécas e as mensagens que serão usadas
import rospy
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped

gapArray = [] #definindo a variavel global que será compartilhada, assim 
bestGapTu = ()

def corrigeGap(lista, valorMin, x = 3):
    """
    Entradas são a lista de valores lidos pelo lidar o valorMinimo que é um float, e x que é um inteiro. 
    Retorna a lista transformando todos os valores menores do que o valor minimo, e x de seus adjacentes em 0
    Ordem de grandeza máximo (2x+1)n+n -> O(n)
    Funciionamento: Varre a lista guardando o index dos valoress menores ou iguais ao valorMin em uma lista. Depois, 
    usando essa lista de indexamentos, a função modifica o valor indexado e x valores, para mais e menos, para zero.
    """
    newlista= []
    for c in range(len(lista)):
        if lista[c] <= valorMin:
            newlista.append(c)
    for n in newlista:
        for i in range(2*x+1):
            a=(n + x - i)
            if   a >= 0 and a < len(lista):
                lista[a] = 0
                
    #print str(lista) #print para testes
    return lista

def callback(msg):
    '''
    Função que é ativada a cada leitura do scan e atualiza a "gap array" 
    aumentando os obstáculos proximos para auxiliar a escolha da melhor direção.
    '''
    global gapArray 
    #define-se o arco de visão onde estamos procurando os obstáculos, e a menor distância entre o carro e os obstáculos.
    rangeMax=int(270*1080/360)  
    rangeMin=int(90*1080/360)
    minDist=2.0
    
    
    
    
    #transformar em lista a tupple de valores de msgs.ranges adquiridas do Lidar
    t=len(msg.ranges)
    tempList=[round(msg.ranges[i], 3) for i in range(t) if (i>rangeMin and i<rangeMax)] 
    
    #função para retornar a lista de leituras com as lacunas sendo valores diferentes de zero
    dist = corrigeGap(tempList, minDist)
    
    #rospy.loginfo(str(dist)) #usado para teste
    
    #atualiza o gapArray com o melhor
    gapArray=dist[:]
    
    
    
    
def melhorGap(listaGaps):
    """
    Entrada é uma lista de valores de lacunas e zeros. 
    Retornar um tuple com o primeiro valor sendo o index central do melhor lacuna de não zeros dessa lista, 
    o segundo valor sendo o numero de valores tem essa lacuna, o terceiro o valor da média desses numeros, e o 
    quarto o numero de valores que tem a lista.
    Ordem de grandeza -> O(n²)
    """
    
    melhorTupla=(0, 0, 0, 0)
    tamLista=len(listaGaps)
    for v in range(len(listaGaps)):
        listaNova=[]
        med = 0
        centro=0
        tamLac=0
        if listaGaps[v] > 0:
            for i in range(len(listaGaps)-v):
                if listaGaps[v+i]>0:
                    listaNova.append(listaGaps[v+i])
                else:
                    break
            tamLac=len(listaNova)
            med=sum(listaNova)/len(listaNova)
            centro=v+int(len(listaNova)/2)
            if tamLac>melhorTupla[1] or (tamLac==melhorTupla[1] and med>melhorTupla[2]):
                melhorTupla=(centro, tamLac, med, tamLista)
    
    #print str(melhorTupla)     #usado para teste   
    return melhorTupla


class FollowTheGap(object):
    
    direc_msg = AckermannDriveStamped()
    
    def __init__(self):
        
        rospy.init_node('follow_gap_node')
        
        self.sub = rospy.Subscriber('/scan', LaserScan, callback)
        
        
        # Aqui eh declarada a mensagem que sera enviada para o software e vai manter o carro 			
        #andando em linha reta.
        direc_msg = AckermannDriveStamped()
        direc_msg.drive.steering_angle = 0
        direc_msg.drive.speed = 1
        
        # Aqui eh feito um loop constante que envia o carro sempre para frente
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            global drive_pub
            global gapArray
            """
            gapTuple=melhorGap(gapArray)
            #direc_msg.drive.steering_angle = 0
           
            #if (gapTuple[0] > (gapTuple[3]/2)+5) or (gapTuple[0] < (gapTuple[3]/2)-5):
            #    direc_msg.drive.steering_angle = (gapTuple[0]-int(gapTuple[3]/2))*0.005823
            #    direc_pub.publish(direc_msg)
            #else:
            #    direc_pub.publish(direc_msg)
            
            mod = (gapTuple[0]-int(gapTuple[3]/2))*0.005823
            if mod>0.4:
                direc_msg.drive.steering_angle = 0.4
            elif mod<-0.4:
                direc_msg.drive.steering_angle = -0.4
            else:
                direc_msg.drive.steering_angle = (gapTuple[0]-int(gapTuple[3]/2))*0.005823
           
            gap_pub.publish(direc_msg)
            
            print str(direc_msg.drive.steering_angle)
            print str(gapTuple)
            rate.sleep()
            """
    
    
    def shutdown(self):
        global direc_msg
        rospy.loginfo("Parada")
        
        shut_msg = AckermannDriveStamped()
        shut_msg.drive.speed = 0
        shut_msg.drive.steering_angle = 0
        gap_pub.publish(shut_msg)
        
        rospy.sleep(1)
def main():
      
    fg = FollowTheGap()
    rospy.spin()
    
# O drive_pub foi declarado global para que ele possa ser usado tando no construtor quanto na funcao. callback
gap_pub = rospy.Publisher('/drive', AckermannDriveStamped, queue_size=10)

main()