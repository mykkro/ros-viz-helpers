import sys
import time
import numpy as np
import pandas as pd
from pathlib import Path
import keyboard
# Pinocchio
import pinocchio as pin
from pinocchio.visualize import MeshcatVisualizer
# Meshcat
import meshcat
import meshcat.geometry as g
import meshcat.transformations as tf
import meshcat_shapes
import tempfile
from numpy.linalg import pinv


from commandr import Commandr
from computer import extract_vectors, add_new_column, set_value, compute

# Example usage:
#  python compute_light.py -i target/move_y.csv -u panda/urdf/panda2_inertias.urdf -o target/move_y_comp.csv


cmdr = Commandr("compute", title="Compute")
cmdr.add_argument("input", "-i", type="str")
cmdr.add_argument("output", "-o", type="str", required=True)
cmdr.add_argument("urdf", "-u", type="str", required=True)

args, configs = cmdr.parse()

input_path = args["input"]
output_path = args["output"]
default_urdf_path = args["urdf"]

compute(input_path, output_path, default_urdf_path)


