#!/usr/bin/env python
import rospy

from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan


def GoFast(msg):


	indice_90graus = 90*1080/180

	DistX = round(msg.ranges[indice_90graus],4)
	TimeStamp = round(GetTimeStamp(msg),3)

	global drive_pub

	go_fast_msg = AckermannDriveStamped()
	go_fast_msg.drive.speed = 3
	go_fast_msg.drive.steering_angle = 0
	drive_pub.publish(go_fast_msg)
	#print "Going fast... xd"

def GetTimeStamp(msg):
	seconds = str(msg.header.stamp.secs-int(1.6e9))
	nseconds = str(msg.header.stamp.nsecs)
	return float(seconds + "." + nseconds)


class go_fast_sys(object):

	# def __init__ eh o construtor da classe go_fast_sys.
	def __init__(self):

		# Aqui eh declarado o objeto que esta inscrito no topico /scan.
		lidar_sub = rospy.Subscriber('/scan', LaserScan, GoFast)

		drive_msg = AckermannDriveStamped()
		drive_msg.drive.speed = 3
		drive_msg.drive.steering_angle = 0

		# Aqui eh feito um loop constante que envia o carro sempre para frente
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			global drive_pub
			drive_pub.publish(drive_msg)
			rate.sleep()

def main():
	# Aqui eh declarado o nome do node.
	rospy.init_node('go_fast')
	go_fast = go_fast_sys()
	rospy.spin()

# O drive_pub foi declarado global para que ele possa ser usado tando no construtor quanto na funcao de callback
drive_pub = rospy.Publisher('/go_fast', AckermannDriveStamped, queue_size=10)

main()
