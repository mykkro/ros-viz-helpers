from pathlib import Path

from rosbags.highlevel import AnyReader
import yaml
import pandas as pd
from commandr import Commandr
from utils import guess_msgtype, register_custom_types

def extract(o, h, key, value):
    # is value list-like?
    try:
        value = list(value)
        for i in range(len(value)):
            fname = f"{key}.{i}"
            o[fname] = value[i]
            h.append(fname)
    except:
        h.append(key)
        o[key] = value


if __name__ == "__main__":

    # Reads rosbag file and saves specified fields into CSV file.

    # Example usage:
    #  python rosbag_fieldextract.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag -o target/move_x.csv -f name -f velocity
    # python rosbag_fieldextract.py -i /home/ros/devel/RoboDemos/bagfiles/ee_force_1/ -o target/EE_FORCE_EXTRACTED.csv -t /mytopic -m dummy_control_msgs/msg/DummyControlDebug.msg -f timestamp -f position -f velocity -f effort -f calc_force


    cmdr = Commandr("ros1bag2csv", title="ROS1 bag to CSV")
    cmdr.add_argument("input", "-i", type="str", required=True)
    cmdr.add_argument("output", "-o", type="str", required=True)
    cmdr.add_argument("topic", "-t|--topic", default="/joint_states")
    cmdr.add_argument("timecol", "--timecol", type="str", default="time_ns") 
    cmdr.add_argument("field", "-f|--field", nargs="*", type="str", default=None)
    cmdr.add_argument("msgpath", "-m|--msgpath", nargs="*", type="str")

    args, configs = cmdr.parse()

    input_path = args["input"]
    output_path = args["output"]
    topic = args["topic"]
    timecol = args["timecol"]
    fields = args["field"]
    msgpaths = args["msgpath"]

    # If no fields were specified, use these default fields:
    if not fields:
        fields = ["name", "position", "velocity", "effort"]

    print(f"Input path:     {input_path}")
    print(f"Output path:    {output_path}")
    print(f"Topic:          {topic}")
    print(f"Fields:         {fields}")

    register_custom_types(msgpaths)
    
    file = Path(input_path)
    dataset_name = file.name
    tbl = []
    header = None
    with AnyReader([file]) as reader:
        for connection, timestamp, rawdata in reader.messages(connections=reader.connections):
            topic_read = connection.topic
            if topic_read == topic:
                msg = reader.deserialize(rawdata, connection.msgtype)

                #time_stamp = msg.header.stamp
                #time_ns = #int(time_stamp.sec * 1e9 + time_stamp.nanosec)

                o = dict()#time_ns=time_ns)
                # Sets time header
                h = []
                # Finds specified fields in the bag and extracts data from them
                for field in fields:
                    attr = getattr(msg, field)
                    print(f"attr {attr} field {field}")
                    extract(o, h, field, attr)
                # Appends data
                header = h
                tbl.append(o)
    # Saves data to CSV
    df = pd.DataFrame(tbl)
    df.to_csv(output_path, columns=header, index=False)

