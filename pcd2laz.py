#!/usr/bin/python3.8
import rosbag
import os
import argparse
import ros_numpy
import laspy
import numpy as np
from os.path import join as opj

# b = bagreader('./20221221_six.bag')
def read_bag(filename):
    bag = rosbag.Bag(filename)
    return bag

def main(filename):

    bag = read_bag(filename)
    basename = os.path.splitext(filename)[0]

    if not os.path.isdir(basename):
        os.makedirs(basename)
    
    i = 0
    for topic, msg, t in bag.read_messages(topics = ['/velodyne_points']):
        sq = str(msg.header.seq)
        m = ros_numpy.point_cloud2.pointcloud2_to_array(msg)

        #creating lasfile
        hdr = laspy.LasHeader()
        hdr.offset = np.floor((np.min(m['x']), np.min(m['y']),np.min(m['z'])))
        hdr.scale = np.array([0.01,0.01,0.01])
        data = laspy.LasData(hdr)
        data.x = m['x']
        data.y = m['y']
        data.z = m['z']
        data.intensity = m['intensity']
        data.write(opj(basename, f'{sq}.laz'))


def parse_arguments():
    argparser = argparse.ArgumentParser(description='Rosbag file with Pointcloud messages.')
    argparser.add_argument("-f","--filename", type=str, required = True ,help='filename')
    args = argparser.parse_args()
    return args

if __name__ == "__main__":
    filename = parse_arguments().filename
    main(filename)

