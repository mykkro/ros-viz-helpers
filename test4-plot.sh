#!/bin/bash

# Plot data

for FILE in move_x move_y move_z rot_x rot_y rot_z
do
    python display-timeseries.py -i target/${FILE}_comp.csv -f 'q.*' -f 'dq.*' -f 'tau_J.*' -o target/${FILE}.q.png 
    python display-timeseries.py -i target/${FILE}_comp.csv -f 'ee_pos.*' -f 'ee_rot_xyzw.*' -o target/${FILE}.ee.png 
done
