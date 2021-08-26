#!/usr/bin/env
from pickle import TRUE
import rospy
from std_msgs.msg import String
from tutorials.msg import Position

def callback(data):
    # rospy.loginfo('Received data: %s', data.data)
    rospy.loginfo('%s X: %f Y: %f', data.message, data.x, data.y)

def listener():
    rospy.init_node('subscriber_node', anonymous=True)
    rospy.Subscriber('greating_topic', Position, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass