#!/usr/bin/env python
import rospy
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
import ros_numpy
import pyrealsense2 as rs2
if (not hasattr(rs2, 'intrinsics')):
    import pyrealsense2.pyrealsense2 as rs2

####DNDB####
import torch
import models
import utils
import dataset
import importers
import argparse
import os
import sys
import argparse

from supervision import *
from exporters import *
from importers import *

import datetime

import torch.nn.functional as F

from models import AE
from supervision import *
from exporters import *
from utils import *
from models.shallow_partial import *


class VideoStreamer:
    """
    Video streamer that continuously is reading frames through subscribing to d435 images.
    Frames are then ready to read when program requires.
    """
    def __init__(self, pub, video_file=None):
        self._pub = pub
        self.colour_retrieved = False
        self.depth_retrieved = False
        self.intrin_retrieved = False
        self.color_image = np.zeros([480,640,3], dtype=np.uint8)
        self.depth_image = np.zeros([480,640], dtype=np.uint8)

    def read(self):
        return (self.color_image, self.depth_image)

    def colour_callback(self, msg):
        if not self.colour_retrieved:
            im = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
            # inverse rgb to bgr
            im = im[:,:,::-1]
            self.color_image = im
            self.colour_retrieved = True
    
    def depth_callback(self, msg):
        if not self.depth_retrieved:
            im = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
            self.depth_image = im[:,:,1]
            self.depth_retrieved = True

    def intrin_callback(self, cameraInfo):
        """
        D435/D435i camera intrinsic values can be derived from CameraInfo ROS message.
        """
        if not self.intrin_retrieved:
            self.intrin = rs2.intrinsics()
            self.intrin.width = cameraInfo.width
            self.intrin.height = cameraInfo.height
            self.intrin.ppx = cameraInfo.K[2]
            self.intrin.ppy = cameraInfo.K[5]
            self.intrin.fx = cameraInfo.K[0]
            self.intrin.fy = cameraInfo.K[4]
            #self.intrin.model = cameraInfo.distortion_model
            self.intrin.model  = rs2.distortion.none     
            self.intrin.coeffs = [i for i in cameraInfo.D]
            self.intrin_retrieved = True

    def set_not_retrieved(self):
        self.colour_retrieved = False
        self.depth_retrieved = False
        self.intrin_retrieved = False

    def publish(self, image):
        # Convert image array to smassage from sensor_msgs
        img_msg = ros_numpy.msgify(Image, image, encoding='mono8')
        self._pub.publish(img_msg)

def talk_to_me():
    pub = rospy.Publisher('greating_topic', String, queue_size=10)
    rospy.init_node('publisher_node', anonymous=True)
    rate = rospy.Rate(1)
    rospy.loginfo('Publisher Node Started, now publishing msgs...')
    while not rospy.is_shutdown():
        msg = 'Hello - %s' % rospy.get_time()
        pub.publish(msg)
        rate.sleep()

def callback(image_data):
    rospy.loginfo('Received data: %s', rospy.get_time())
    im = np.frombuffer(image_data.data, dtype=np.uint8).reshape(image_data.height, image_data.width, -1)
    # cv2.imwrite('output/omg.png', im)
    # plt.imshow(im)
    # plt.imsave('src/denoising/output/%s.png' % rospy.get_time(), im)
    # plt.show()
    rospy.loginfo(im.shape)
    # rospy.loginfo('Received data: %s', image_data.data)

def listener():
    rospy.init_node('subscriber_node', anonymous=True)
    rospy.Subscriber('/camera/color/image_raw', Image, callback)
    rospy.Subscriber("/camera/depth/image_rect_raw", Image, callback)
    # rospy.Subscriber("/camera/depth/camera_info", CameraInfo, callback)

    rospy.spin()

if __name__ == '__main__':
    # try:
    #     listener()
    # except rospy.ROSInterruptException:
    #     pass

    # publish a ROS topic of the denoised & deblurred depth results
    pub = rospy.Publisher('DNDB_depth', Image, queue_size=1)

    # initial node
    rospy.init_node('ros_dndb')

    rospy.loginfo('ros_dndb Node Started, now publishing msgs...')

    # Initialise video streams from D435
    video_streamer = VideoStreamer(pub)

    """
    This is the ROS topic to get images from. If no image is being found, type
    'rostopic list' in the console to find available topics. It may be called 
    '/d400/color/image_raw' instead.
    """
    rospy.Subscriber("/d400/color/image_raw", Image, video_streamer.colour_callback)
    rospy.Subscriber("/d400/aligned_depth_to_color/image_raw", Image, video_streamer.depth_callback)
    rospy.Subscriber("/d400/depth/camera_info", CameraInfo, video_streamer.intrin_callback)

    while True:
        color_img, depth_img = video_streamer.read()





        video_streamer.publish(depth_img)
        video_streamer.set_not_retrieved()

