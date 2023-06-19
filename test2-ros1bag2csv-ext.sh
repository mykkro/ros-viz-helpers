#!/bin/bash

# Gather /franka_state_controller/franka_states from ROS1 bag files and export CSV files from them.

python ros1bag2csv-ext.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag -o target/move_x.csv
python ros1bag2csv-ext.py -i d:/backup/2023-06-16/ros1-dumps/move_y_plus_minus.bag -o target/move_y.csv
python ros1bag2csv-ext.py -i d:/backup/2023-06-16/ros1-dumps/move_z_plus_minus.bag -o target/move_z.csv
python ros1bag2csv-ext.py -i d:/backup/2023-06-16/ros1-dumps/rot_x.bag -o target/rot_x.csv
python ros1bag2csv-ext.py -i d:/backup/2023-06-16/ros1-dumps/rot_y.bag -o target/rot_y.csv
python ros1bag2csv-ext.py -i d:/backup/2023-06-16/ros1-dumps/rot_z.bag -o target/rot_z.csv
