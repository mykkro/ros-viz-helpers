from pathlib import Path

from rosbags.highlevel import AnyReader
import yaml
import pandas as pd
from commandr import Commandr
from utils import guess_msgtype, register_custom_types
from fieldextract import fieldextract, extract 


cmdr = Commandr("ros1bag2csv", title="ROS1 bag to CSV")
cmdr.add_argument("input", "-i", type="str", required=True)
cmdr.add_argument("output", "-o", type="str", required=True)
cmdr.add_argument("topic", "-t|--topic", default="/joint_states")
cmdr.add_argument("timecol", "--timecol", type="str", default="time_ns") 
cmdr.add_argument("field", "-f|--field", nargs="*", type="str", default=None)
cmdr.add_argument("msgpath", "-m|--msgpath", nargs="*", type="str")

args, configs = cmdr.parse()

input_path = args["input"]
output_path = args["output"]
topic = args["topic"]
timecol = args["timecol"]
fields = args["field"]
msgpaths = args["msgpath"]

# Example usage:
    # python rosbag_fieldextract.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag -o target/move_x.csv -f name -f velocity
    # python rosbag_fieldextract.py -i /home/ros/devel/RoboDemos/bagfiles/ee_force_1/ -o target/EE_FORCE_EXTRACTED.csv -t /mytopic -m dummy_control_msgs/msg/DummyControlDebug.msg -f timestamp -f position -f velocity -f effort -f calc_force

fieldextract(input_path, output_path, topic, fields, msgpaths)