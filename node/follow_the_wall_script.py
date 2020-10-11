#!/usr/bin/env python
import rospy
import math

from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan

erro_anterior = 0

# Essa funcao eh chamada toda vez que um evento do topico /scan eh publicado
def callback(msg):

	# O LIDAR mede 360 graus e o vetor eh anti horario (0 eh em baixo e 90 graus eh a direita)
	# Alem disso, o LIDAR retorna o seu valor em metros 1:1 com a 'realidade'

	# Como nao sabemos a largura da pista, vai ser feito um algoritmo para medir o meio da pista
	# Vamos considerar a parede da esquerda para o algoritmo 
	indice_90graus = 90*1080/360
	indice_135graus = 135*1080/360
	indice_180graus = 180*1080/360
	indice_235graus = 235*1080/360
	indice_270graus = 270*1080/360

	
	# para o carro ficar no meio o set point sera calculado a cada iteracao
	distancia_direita = msg.ranges[indice_90graus]
	distancia_esquerda = msg.ranges[indice_270graus]

	theta = 45
	set_point = (distancia_direita + distancia_esquerda)/2

	a = msg.ranges[indice_235graus]
	b = msg.ranges[indice_270graus]

	alpha = math.atan((a*math.cos(theta)-b)/(a*math.sin(theta)))
	AB = b*math.cos(alpha)

	# AC eh a distancia que o carro eh projetado
	AC = 0.5
	CD = AB + AC*math.sin(alpha)

	## Segundo calculo da posicao
	#c = msg.ranges[indice_135graus]
	#d = msg.ranges[indice_90graus]

	#alpha2 = math.atan((c*math.cos(theta)-d)/(c*math.sin(theta)))
	#AB2 = d*math.cos(alpha2)

	#CD2 = AB2 + AC*math.sin(alpha2)

	#print(AB)	

	Kp = 2
	Kd = 1
	
	#erro_atual = set_point - (CD+CD2)/2
	erro_atual = set_point - CD
	global erro_anterior

	acao_de_controle = Kp*erro_atual+Kd*(erro_atual - erro_anterior)
	
	# Vai existir um controle de velocidade que vai ver o quanto de espaco que ele tem pra frente e vai acelerar a partir disso

	wall_avoid_msg = AckermannDriveStamped()
	
	#wall_avoid_msg.drive.speed = -7/10*erro_atual+5

	if(msg.ranges[indice_180graus] > 15):	
		wall_avoid_msg.drive.speed = 7
	else:
		wall_avoid_msg.drive.speed = 0.7*msg.ranges[indice_180graus]

	global drive_pub

	wall_avoid_msg.drive.steering_angle = -acao_de_controle
	#if(msg.ranges[indice_180graus] > msg.ranges[indice_90graus] and msg.ranges[indice_180graus] > msg.ranges[indice_270graus]):		
	#	wall_avoid_msg.drive.steering_angle = acao_de_controle
	#elif(msg.ranges[indice_180graus] < msg.ranges[indice_90graus]):
	#	wall_avoid_msg.drive.steering_angle = -0.3
	#elif(msg.ranges[indice_180graus] < msg.ranges[indice_180graus]):
	#	wall_avoid_msg.drive.steering_angle = 0.3

	drive_pub.publish(wall_avoid_msg)

	# max_speed: 7. #  meters/second
	# max_steering_angle: 0.4189 # radians / 24 degree
	#EH NECESSaRIO VER OS LIMITES DO STEERING_ANGLE E DA VELOCIDADE PARA AJUSTAR O CONTROLADOR
	erro_anterior = erro_atual
	

	

	#if msg.ranges[indice_45graus] < 0.5:		
		#wall_avoid_msg.drive.steering_angle = 0.5
		#drive_pub.publish(wall_avoid_msg)


class WallAvoid(object):
    
	def __init__(self):
		
		wa_sub = rospy.Subscriber('/scan', LaserScan, callback)

		drive_msg = AckermannDriveStamped()
		drive_msg.drive.steering_angle = 0
		drive_msg.drive.speed = 4
		print("bolota")
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			global drive_pub
			drive_pub.publish(drive_msg)
			rate.sleep()
			#print("bolota")
def main():
	rospy.init_node('follow_the_wall_node')
	wa = WallAvoid()
	rospy.spin()


# O drive_pub foi declarado global para que ele possa ser usado tando no construtor quanto na funcao. callback
drive_pub = rospy.Publisher('/follow_the_wall', AckermannDriveStamped, queue_size=10)

main()
