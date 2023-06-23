from pathlib import Path

from rosbags.highlevel import AnyReader
import yaml
import pandas as pd
from commandr import Commandr


def extract(o, h, key, value):
    for i in range(len(value)):
        fname = f"{key}.{i}"
        o[fname] = value[i]
        h.append(fname)


if __name__ == "__main__":

    # Reads topic (/franka_state_controller/franka_states) from ROS1 bag file. Saves position, velocity, effort data to CSV files.

    # Example usage:
    #  python ros1bag2csv-ext.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag -o target/move_x.csv


    cmdr = Commandr("ros1bag2csv", title="ROS1 bag to CSV")
    cmdr.add_argument("input", "-i", type="str", required=True)
    cmdr.add_argument("output", "-o", type="str", required=True)
    cmdr.add_argument("topic", "-t|--topic", default="/franka_state_controller/franka_states")
 
    args, configs = cmdr.parse()

    input_path = args["input"]
    output_path = args["output"]
    topic = args["topic"]

    print(f"Input path:     {input_path}")
    print(f"Output path:    {output_path}")
    print(f"Topic:          {topic}")

    file = Path(input_path)
    dataset_name = file.name
    tbl = []
    header = None
    with AnyReader([file]) as reader:
        for connection, timestamp, rawdata in reader.messages(connections=reader.connections):
            topic_read = connection.topic
            if topic_read == topic:
                msg = reader.deserialize(rawdata, connection.msgtype)

                time_stamp = msg.header.stamp
                time_ns = int(time_stamp.sec * 1e9 + time_stamp.nanosec)

                o = dict(time_ns=time_ns)
                h = ["time_ns"]
                extract(o, h, "q", list(msg.q))
                extract(o, h, "dq", list(msg.dq))
                extract(o, h, "tau_J", list(msg.tau_J))
                extract(o, h, "dtau_J", list(msg.dtau_J))
                extract(o, h, "O_T_EE", list(msg.O_T_EE))  #  Measured end effector pose in base frame.
                # extract(o, h, "O_T_EE_c", list(msg.O_T_EE_c))  #  Last commanded end effector pose of motion generation in base frame.
                extract(o, h, "EE_T_K", list(msg.EE_T_K))  #  Stiffness frame pose in end effector frame.
                extract(o, h, "F_T_EE", list(msg.F_T_EE))  #  End effector frame pose in flange frame.
                extract(o, h, "O_F_ext_hat_K", list(msg.O_F_ext_hat_K))  # Estimated external wrench (force, torque) acting on stiffness frame, expressed relative to the base frame.
                extract(o, h, "K_F_ext_hat_K", list(msg.K_F_ext_hat_K))  # Estimated external wrench (force, torque) acting on stiffness frame, expressed relative to the stiffness frame.
                extract(o, h, "tau_ext_hat_filtered", list(msg.tau_ext_hat_filtered))  # External torque, filtered

                header = h
                tbl.append(o)

    df = pd.DataFrame(tbl)
    df.to_csv(output_path, columns=header, index=False)

