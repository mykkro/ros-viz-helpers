#!/bin/bash

# Compute extra data (ee_pos, ee_rot_xyzw...) and saves as _comp.csv

for FILE in move_x move_y move_z rot_x rot_y rot_z
do
    python compute.py -i target/$FILE.csv -u panda/urdf/panda2_inertias.urdf -o target/${FILE}_comp.csv
done
