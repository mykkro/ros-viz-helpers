## Reading ROS1 and ROS2 bags in Python

* https://github.com/rpng/rosbags

## FrankaState message

* Message definition: https://github.com/frankaemika/franka_ros/blob/develop/franka_msgs/msg/FrankaState.msg
* Meaning of individual fields explained here: https://frankaemika.github.io/docs/franka_ros.html
* Struct reference: https://frankaemika.github.io/libfranka/structfranka_1_1RobotState.html

## Setup and install

```bash
conda activate ros1

pip install -r requirements.txt

# Install helper libraries (kommons and commandr)
(cd kommons && python setup.py install)
(cd commandr && python setup.py install)

# Install Pinocchio for Python
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install pinocchio

# Tested under Windows 10 + Git Bash... OK
```

## 1. Get data from ROS1 bag and export to CSV

Export joint state data:
* position
* velocity
* effort

to three separate files: `*_q.csv`, `*_v.csv`, `*_tau.csv`.

```bash
python ros1bag2csv.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag -o target/move_x

# This will create three files: target_move_x_q.csv, target_move_x_v.csv, target_move_x_tau.csv.
```
