#!/bin/bash

# Gather /joint_states from ROPS1 bag files and export _q, _v, _tau CSV files from them.

python ros1bag2csv.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag -o target/move_x
python ros1bag2csv.py -i d:/backup/2023-06-16/ros1-dumps/move_y_plus_minus.bag -o target/move_y
python ros1bag2csv.py -i d:/backup/2023-06-16/ros1-dumps/move_z_plus_minus.bag -o target/move_z
python ros1bag2csv.py -i d:/backup/2023-06-16/ros1-dumps/rot_x.bag -o target/rot_x
python ros1bag2csv.py -i d:/backup/2023-06-16/ros1-dumps/rot_y.bag -o target/rot_y
python ros1bag2csv.py -i d:/backup/2023-06-16/ros1-dumps/rot_z.bag -o target/rot_z
