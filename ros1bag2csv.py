from pathlib import Path

from rosbags.highlevel import AnyReader
import yaml
import pandas as pd
from commandr import Commandr



if __name__ == "__main__":

    # Reads topic (/joint_states by default) from ROS1 bag file. Saves position, velocity, effort data to CSV files.

    # Example usage:
    #  python ros1bag2csv.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag -o target/move_x


    cmdr = Commandr("ros1bag2csv", title="ROS1 bag to CSV")
    cmdr.add_argument("input", "-i", type="str", required=True)
    cmdr.add_argument("output", "-o", type="str", required=True)
    cmdr.add_argument("topic", "-t|--topic", default="/joint_states")
 
    args, configs = cmdr.parse()

    input_path = args["input"]
    output_prefix = args["output"]
    topic = args["topic"]

    print(f"Input path:     {input_path}")
    print(f"Output prefix:  {output_prefix}")
    print(f"Topic:          {topic}")

    file = Path(input_path)
    dataset_name = file.name
    tbl_q = []
    tbl_v = []
    tbl_tau = []
    with AnyReader([file]) as reader:
        for connection, timestamp, rawdata in reader.messages(connections=reader.connections):
            topic_read = connection.topic
            if topic_read == topic:
                msg = reader.deserialize(rawdata, connection.msgtype)

                time_stamp = msg.header.stamp
                time_ns = int(time_stamp.sec * 1e9 + time_stamp.nanosec)

                names =list(msg.name)
                positions = list(msg.position)
                velocities = list(msg.velocity)
                efforts = list(msg.effort)

                tbl_q.append(dict(zip(["time_ns"] + names, [time_ns] + positions)))
                tbl_v.append(dict(zip(["time_ns"] + names, [time_ns] + velocities)))
                tbl_tau.append(dict(zip(["time_ns"] + names, [time_ns] + efforts)))

        df_q = pd.DataFrame(tbl_q)
        df_v = pd.DataFrame(tbl_v)
        df_tau = pd.DataFrame(tbl_tau)

        df_q.to_csv(f"{output_prefix}_q.csv", index=False)
        df_v.to_csv(f"{output_prefix}_v.csv", index=False)
        df_tau.to_csv(f"{output_prefix}_tau.csv", index=False)
