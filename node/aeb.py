#!/usr/bin/env python
import rospy

from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan


def CheckTTC(msg):

	global NotTriggered

	if CheckTTC.Count == 125:

		indice_90graus = 90*1080/180

		DistX = round(msg.ranges[indice_90graus],4)
		TimeStamp = round(GetTimeStamp(msg),3)

		VelX = round((DistX - CheckTTC.DistX_LastMsg)/(TimeStamp - CheckTTC.TimeStamp_LastMsg),4)

		# if NotTriggered:
		#
		# 	print "DistX: " + str(DistX) + " DistX_LM: " + str(CheckTTC.DistX_LastMsg)
		# 	print "dx: " + str(DistX - CheckTTC.DistX_LastMsg)
		# 	print "TS: " + str(TimeStamp) + " TS_LM: " + str(CheckTTC.TimeStamp_LastMsg)
		# 	print "dt: " + str(TimeStamp - CheckTTC.TimeStamp_LastMsg)
		# 	print "VelX: " + str(VelX)
		# 	print "TTC: " + str(CheckTTC.TTC)

		CheckTTC.TimeStamp_LastMsg = TimeStamp
		CheckTTC.DistX_LastMsg = DistX
		CheckTTC.Count = 0

		if VelX < 0:
			CheckTTC.TTC = -DistX/VelX

	CheckTTC.Count += 1

	# Aqui eh chamado o publicador global.
	global drive_pub

	if CheckTTC.TTC < CheckTTC.TTCmin:
		aeb_msg = AckermannDriveStamped()
		aeb_msg.drive.speed = 0
		aeb_msg.drive.steering_angle = 0
		drive_pub.publish(aeb_msg)
		if NotTriggered:
			#print "AEB triggered"
			NotTriggered = False

CheckTTC.TimeStamp_LastMsg = 0;
CheckTTC.DistX_LastMsg = 0;
CheckTTC.Count = 0;
CheckTTC.TTCmin = 3;
CheckTTC.TTC = 1e3;

NotTriggered = True

def GetTimeStamp(msg):
	seconds = str(msg.header.stamp.secs-int(1.6e9))
	nseconds = str(msg.header.stamp.nsecs)
	return float(seconds + "." + nseconds)


class aeb_system(object):

	# def __init__ eh o construtor da classe aeb_system.
	def __init__(self):

		# Aqui eh declarado o objeto que esta inscrito no topico /scan.
		lidar_sub = rospy.Subscriber('/scan', LaserScan, CheckTTC)

		# Aqui eh declarada a mensagem que sera enviada para o software e vai manter o carro andando em linha reta.
		if NotTriggered:
			drive_msg = AckermannDriveStamped()
			drive_msg.drive.steering_angle = 0
			drive_msg.drive.speed = 0.3

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

# O drive_pub foi declarado global para que ele possa ser usado tando no construtor quanto na funcao de callback
drive_pub = rospy.Publisher('/aeb_sys', AckermannDriveStamped, queue_size=10)

main()
