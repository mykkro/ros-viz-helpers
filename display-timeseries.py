from pathlib import Path

from rosbags.highlevel import AnyReader
import yaml
import pandas as pd
from commandr import Commandr
import matplotlib.pyplot as plt
from timeseries import match_pattern, match_columns, timeseriesplot

# Time Series plotter.

# Example usage:
#  python display-timeseries.py -i target/move_x.csv -f 'q.*' -f 'dq.*' -f 'tau_J.*'
#  python display-timeseries.py -i target/move_x.csv -f 'O_T_EE.12,O_T_EE.13,O_T_EE.14' 
#  python display-timeseries.py -i target/move_x.csv -f 'q.*' -f 'dq.*' -f 'tau_J.*' --from 100 --to 300 -o target/move_x.q.png
#  python display-timeseries.py -i target/move_y_comp.csv -f 'ee_pos.*' -f 'ee_rot_xyzw.*' -o target/move_y.ee.png --from 100 --to 500 --plo
# python display-timeseries.py -i target/EE_FORCE_EXTRACTED.csv -f "position.*" -f "effort.*" -f "calc_force.0,calc_force.1,calc_force.2" --plot


cmdr = Commandr("display-timeseries", title="ROS1 bag to CSV")
cmdr.add_argument("input", "-i", type="str", required=True)
cmdr.add_argument("output", "-o", type="str", required=False)
cmdr.add_argument("field", "-f|--field", nargs="*")
cmdr.add_argument("fromframe", "--from", type='int', default=0)
cmdr.add_argument("toframe", "--to", type='int', default=-1)
cmdr.add_argument("plot", "--plot", type='switch')

args, configs = cmdr.parse()

input_path = args["input"]
output_path = args["output"]
fields = args["field"]
from_frame = args["fromframe"]
to_frame = args["toframe"]
shall_plot = args["plot"]

timeseriesplot(input_path, output_path, fields, from_frame, to_frame, shall_plot)