#!/bin/bash

# Gather /joint_states from ROPS1 bag files and export _q, _v, _tau CSV files from them.

DUMPDIR=dumps/ros1-dumps
python ros1bag2csv.py -i $DUMPDIR/move_x_plus_minus.bag -o target/move_x
python ros1bag2csv.py -i $DUMPDIR/move_y_plus_minus.bag -o target/move_y
python ros1bag2csv.py -i $DUMPDIR/move_z_plus_minus.bag -o target/move_z
python ros1bag2csv.py -i $DUMPDIR/rot_x.bag -o target/rot_x
python ros1bag2csv.py -i $DUMPDIR/rot_y.bag -o target/rot_y
python ros1bag2csv.py -i $DUMPDIR/rot_z.bag -o target/rot_z
