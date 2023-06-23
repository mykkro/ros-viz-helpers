import sys
import time
import numpy as np
import pandas as pd
from pathlib import Path
# Pynput
from pynput import keyboard
from pynput.keyboard import Key
# Pinocchio
import pinocchio as pin
from pinocchio.visualize import MeshcatVisualizer
# Meshcat
import meshcat
import meshcat.geometry as g
import meshcat.transformations as tf
import meshcat_shapes
import tempfile


from commandr import Commandr
from trajvizualizer import visualizetrajectory

# Animates Panda robot based on joint states read from CSV file.

# Example usage:
#  python trajviz.py -i target/move_y_q.csv -u panda/urdf/panda2_inertias.urdf


cmdr = Commandr("trajviz", title="ROS1 bag to CSV")
cmdr.add_argument("input", "-i", type="str", required=True)
cmdr.add_argument("urdf", "-u", type="str", required=True)
cmdr.add_argument("speed", "-s|--speed", type='float', default=1.0)
cmdr.add_argument("repeat", "-r|--repeat", type='switch')
cmdr.add_argument("timecol", "-t|--timecol", type="str", default="time_ns")
cmdr.add_argument("poscol", "-p|--poscol", type="str", default="panda_joint1,panda_joint2,panda_joint3,panda_joint4,panda_joint5,panda_joint6,panda_joint7")

args, configs = cmdr.parse()

# Path to Waypoint CSV
traces_csv_path = args["input"]
default_urdf_path = args["urdf"]
speed_coefficient = args["speed"]
repeat = args["repeat"]
timecol = args["timecol"]
poscol = args["poscol"]

visualizetrajectory(traces_csv_path, default_urdf_path, speed_coefficient, repeat, timecol, poscol)