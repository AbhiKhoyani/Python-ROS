import rosbag
import os
import argparse
import ros_numpy
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
    
    f = open(opj(basename,'timestamps.txt'), 'w')
    i = 0
    for topic, msg, t in bag.read_messages(topics = ['/velodyne_points']):
        ts = str(msg.header.stamp)+'\n'
        sq = str(msg.header.seq)
        m = ros_numpy.point_cloud2.pointcloud2_to_array(msg)
        # print(m.shape)
        # m = m[['x','y','z','intensity']]
        x = m['x']
        y = m['y']
        z = m['z']
        intensity = m['intensity']
        arr = np.zeros(x.shape[0] + y.shape[0] + z.shape[0] + intensity.shape[0], dtype=np.float32)
        arr[::4] = x
        arr[1::4] = y
        arr[2::4] = z
        arr[3::4] = intensity
        arr.astype('float32').tofile(opj(basename, f'{sq}.bin'))
        f.write(ts)
        i+=1
        if i%10==0:
            break

    f.close()

def parse_arguments():
    argparser = argparse.ArgumentParser(description='Rosbag file with Pointcloud messages.')
    argparser.add_argument("-f","--filename", type=str, required = True ,help='filename')
    args = argparser.parse_args()
    return args

if __name__ == "__main__":
    filename = parse_arguments().filename
    main(filename)

