# Python-ROS

Run: 
```
python pcd2bin.py -f "xyz.bag"
python pcd2laz.py -f "xyz.bag"
```
This will create the new folder xyz and extract *.bin files and timestamp.txt files inside that folder.
pcd2laz.py will by default creat `sequence.laz` (compressed las) file for saving memory. 

Requirements:
ros_numpy
rosbag
numpy
laspy
