#!/bin/bash

# Plot data

for FILE in move_x move_y move_z rot_x rot_y rot_z
do
    python display-timeseries.py -i target/${FILE}_comp.csv -f 'q.*' -f 'dq.*' -f 'dq_filtered.*' -f 'tau_J.*' -o target/${FILE}.q.png 
    python display-timeseries.py -i target/${FILE}_comp.csv -f 'ee_pos.*' -f 'ee_rot_xyzw.*' -o target/${FILE}.ee.png 
    python display-timeseries.py -i target/${FILE}_comp.csv -f 'tau_J.*' -f 'dtau_J.*' -f 'tau_ext_hat_filtered.*' -o target/${FILE}.tau.png 

    python display-timeseries.py -i target/${FILE}_comp.csv -f 'q.*' -f 'position.0,position.1,position.2,position.3,position.4,position.5,position.6' -o target/${FILE}.pos.png 
    python display-timeseries.py -i target/${FILE}_comp.csv -f 'dq.*' -f 'velocity.0,velocity.1,velocity.2,velocity.3,velocity.4,velocity.5,velocity.6' -o target/${FILE}.vel.png 
    python display-timeseries.py -i target/${FILE}_comp.csv -f 'tau_J.*' -f 'effort.0,effort.1,effort.2,effort.3,effort.4,effort.5,effort.6' -f 'eff_delta.0,eff_delta.1,eff_delta.2,eff_delta.3,eff_delta.4,eff_delta.5,eff_delta.6'  -f 'tau_ext_hat_filtered.*' -o target/${FILE}.eff.png 
done
