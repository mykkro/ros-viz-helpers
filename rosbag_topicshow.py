from pathlib import Path
from rosbags.highlevel import AnyReader
from commandr import Commandr
from rosbags.typesys import get_types_from_msg, register_types
from utils import guess_msgtype, register_custom_types


if __name__ == "__main__":

    # Reads ros bag file and prints out all topics found in it

    # Example usage:
    #  python rosbag_topicshow.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag
    # python rosbag_topicshow.py -i /home/ros/devel/RoboDemos/bagfiles/ee_force_1 -m dummy_control_msgs/msg/DummyControlDebug.msg


    cmdr = Commandr("ros1bag2csv", title="ROS1 bag to CSV")
    cmdr.add_argument("input", "-i", type="str", required=True)
    cmdr.add_argument("msgpath", "-m|--msgpath", nargs="*", type="str")

 
    args, configs = cmdr.parse()

    input_path = args["input"]
    msgpaths = args["msgpath"]

    print(f"Input path:     {input_path}")
    
    register_custom_types(msgpaths)



    file = Path(input_path)
    dataset_name = file.name
    topics = set()
    header = None
    with AnyReader([file]) as reader:
        for connection, timestamp, rawdata in reader.messages(connections=reader.connections):
            topic_read = connection.topic
            if topic_read not in topics:
                print("Deserializing message:", connection.msgtype)
                msg = reader.deserialize(rawdata, connection.msgtype)
                fields = [f for f in list(dir(msg)) if not f.startswith("_")]
                print(f"Topic: {topic_read}")
                print(f"Fields:")
                for f in fields:
                    print("  ", f)
                topics.add(topic_read)
                print()
