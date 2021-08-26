#!/usr/bin/env
from pickle import TRUE
import rospy
from std_msgs.msg import String
from tutorials.msg import Position

def talk_to_me():
    pub = rospy.Publisher('greating_topic', Position, queue_size=10)
    rospy.init_node('publisher_node', anonymous=True)
    rate = rospy.Rate(1)
    rospy.loginfo('Publisher Node Started, now publishing msgs...')
    while not rospy.is_shutdown():
        # msg = 'Hello - %s' % rospy.get_time()
        msg = Position()
        msg.message = 'My position is: '
        msg.x = 2.0
        msg.y = 1.5
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talk_to_me()
    except rospy.ROSInterruptException:
        pass