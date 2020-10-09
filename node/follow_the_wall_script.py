#!/usr/bin/env python
import rospy
import math

from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

# Essa funcao eh chamada toda vez que um evento do topico /scan eh publicado
def callback(msg):

	# Vamos considerar a parede da esquerda para o algoritmo 
	indice_0graus = 0
	indice_45graus = 45*1080/180
	
	b = msg.ranges[indice_0graus]
	a = msg.ranges[indice_45graus]
	theta = 45

	alpha = math.atan((a*math.cos(theta)-b)/(a*math.sin(theta))
	AB = b*math.cos(alpha)
	# AC é a distância que o carro eh projetado
	AC = 0.5
	CD = AB + AC*math.sin(alpha)

	Kp = 1
	Kd = 1
	
	set_point = 5

	erro = set_pint - CD

	#É NECESSÁRIO VER OS LIMITES DO STEERING_ANGLE E DA VELOCIDADE PARA AJUSTAR O CONTROLADOR

	global drive_pub

	wall_avoid_msg = AckermannDriveStamped()
	wall_avoid_msg.drive.speed = 1

	#if msg.ranges[indice_45graus] < 0.5:		
		#wall_avoid_msg.drive.steering_angle = 0.5
		#drive_pub.publish(wall_avoid_msg)


class WallAvoid(object):
    
	def __init__(self):
		
		wa_sub = rospy.Subscriber('/scan', LaserScan, callback)

		drive_msg = AckermannDriveStamped()
		drive_msg.drive.steering_angle = 0
		drive_msg.drive.speed = 1

		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			global drive_pub
			drive_pub.publish(drive_msg)
			rate.sleep()
def main():
	rospy.init_node('follow_the_wall_node')
	wa = WallAvoid()
	rospy.spin()

# O drive_pub foi declarado global para que ele possa ser usado tando no construtor quanto na funcao. callback
drive_pub = rospy.Publisher('/follow_the_wall', AckermannDriveStamped, queue_size=10)

main()
