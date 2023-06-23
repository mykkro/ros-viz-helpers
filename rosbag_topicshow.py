from pathlib import Path
from rosbags.highlevel import AnyReader
from commandr import Commandr
from rosbags.typesys import get_types_from_msg, register_types
from utils import guess_msgtype, register_custom_types
from topicshow import showtopic

# Reads ros bag file and prints out all topics and found in it and their respective fields

# Example usage:
#  python rosbag_topicshow.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag
#  python rosbag_topicshow.py -i /home/ros/devel/RoboDemos/bagfiles/ee_force_1 -m dummy_control_msgs/msg/DummyControlDebug.msg


cmdr = Commandr("ros1bag2csv", title="ROS1 bag to CSV")
cmdr.add_argument("input", "-i", type="str", required=True) 
cmdr.add_argument("msgpath", "-m|--msgpath", nargs="*", type="str", default=None)


args, configs = cmdr.parse()

input_path = args["input"]
msgpaths = args["msgpath"]


showtopic(input_path, msgpaths)
