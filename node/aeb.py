#!/usr/bin/env python
import rospy

#tamo up to date!

# AckermannDriveStamped eh o tipo de mensgem que eh enviada para o simulador para fazer ele se locomover
from ackermann_msgs.msg import AckermannDriveStamped
# LaserScan eh o tipo de mensagem enviada pelo simulador que contem as informacoes do LIDAR
from sensor_msgs.msg import LaserScan

# Essa funcao eh chamada toda vez que um evento do topico /scan eh publicado
def callback(msg):

	# Dentro de msg, existem varios atributos. O mais importante eh o atributo range, que eh um array que contem a leitura dos feixes do sensor LIDAR. Como o atributo possui 1080 valores e o 		alcance do sensor cobre um area de 180 graus ao redor do sensor, sabemos que o valor 0 graus do sensor eh equivalente ao primeiro item do array mas.range[0] e, consequentemente, o ultimo 		valor do array equivale ao angulo de 180 graus.

	# Aqui eh calculado qual eh o item do vetor que informa a leitura do angulo 45 e 135 graus.
	indice_45graus = 45*1080/180
	indice_135graus = 135*1080/180

	# Aqui eh chamado o publicador global.
	global drive_pub

	# Aqui eh declarada a mensagem que fara o carro virar para algum dos lados.
	aeb_msg = AckermannDriveStamped()
	aeb_msg.drive.speed = 1

	# Aqui se verifica se alguma das leituras esta proxima a parede.
	if msg.ranges[indice_45graus] < 0.5:
		aeb_msg.drive.steering_angle = 0.5
		drive_pub.publish(aeb_msg)
		# print "obstaculo a esquerda"
	elif msg.ranges[indice_135graus] < 0.5:
		aeb_msg.drive.steering_angle = -0.5
		drive_pub.publish(aeb_msg)
		# print "obstaculo a direita"


class aeb_system(object):

	# def __init__ eh o construtor da classe aeb_system.
	def __init__(self):

		# Aqui eh declarado o objeto que esta inscrito no topico /scan.
		lidar_sub = rospy.Subscriber('/scan', LaserScan, callback)

		# Aqui eh declarada a mensagem que sera enviada para o software e vai manter o carro 			andando em linha reta.
		drive_msg = AckermannDriveStamped()
		drive_msg.drive.steering_angle = 0
		drive_msg.drive.speed = 1

		# Aqui eh feito um loop constante que envia o carro sempre para frente
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			global drive_pub
			drive_pub.publish(drive_msg)
			rate.sleep()
def main():
	# Aqui eh declarado o nome do node.
	rospy.init_node('aeb_node')
	aeb = aeb_system()
	rospy.spin()

# O drive_pub foi declarado global para que ele possa ser usado tando no construtor quanto na funcao. callback
drive_pub = rospy.Publisher('/aeb_sys', AckermannDriveStamped, queue_size=10)

main()
