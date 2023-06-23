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


def fieldextract(input_path, output_path, topic, fields, msgpaths):

    # If no fields were specified, use these default fields:
    if not fields:
        fields = ["name", "position", "velocity", "effort"]

    if msgpaths != None:
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

                o = dict()
                h = []

                # Finds specified fields in the bag and extracts data from them
                for field in fields:
                    attr = getattr(msg, field)
                    extract(o, h, field, attr)
                # Appends data
                header = h
                tbl.append(o)
    
    # Saves data to CSV
    df = pd.DataFrame(tbl)
    df.to_csv(output_path, columns=header, index=False)

