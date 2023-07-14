from pathlib import Path
from rosbags.highlevel import AnyReader
from commandr import Commandr
from rosbags.typesys import get_types_from_msg, register_types
from core_programs.utils import guess_msgtype, register_custom_types

def showtopic(input_path, msgpaths):

    if msgpaths != None:
        register_custom_types(msgpaths)

    file = Path(input_path)
    dataset_name = file.name
    topics = set()
    header = None
    
    with AnyReader([file]) as reader:
        for connection, timestamp, rawdata in reader.messages(connections=reader.connections):

            topic_read = connection.topic
            
            if topic_read not in topics:
                msg = reader.deserialize(rawdata, connection.msgtype)
                fields = [f for f in list(dir(msg)) if not f.startswith("_")]
                
                print(f"Topic: {topic_read}")
                print(f"Fields:")
                
                for f in fields:
                    print("  ", f)
                topics.add(topic_read)
                print()
