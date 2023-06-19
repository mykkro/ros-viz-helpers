from pathlib import Path

from rosbags.highlevel import AnyReader
import yaml
import pandas as pd
from commandr import Commandr
import matplotlib.pyplot as plt


def match_pattern(field, value):
    if field.endswith("*"):
        field = field.replace("*", '')
        if value.startswith(field):
            return value
    return None


def match_columns(field, columns):
    return list(filter(None, [match_pattern(field, c) for c in columns]))


if __name__ == "__main__":

    # 

    # Example usage:
    #  python ros1bag2csv-ext.py -i d:/backup/2023-06-16/ros1-dumps/move_x_plus_minus.bag -o target/move_x.csv


    cmdr = Commandr("display-timeseries", title="ROS1 bag to CSV")
    cmdr.add_argument("input", "-i", type="str", required=True)
    cmdr.add_argument("output", "-o", type="str", required=False)
    cmdr.add_argument("field", "-f|--field", nargs="*")
 
    args, configs = cmdr.parse()

    input_path = args["input"]
    output_path = args["output"]
    fields = args["field"]

    print(f"Input path:     {input_path}")
    print(f"Output path:    {output_path}")
    print(f"Fields:         {fields}")

    df = pd.read_csv(input_path)
    columns = df.columns

    for group in fields:

        series_names = group.split(",")
        print("series names:", series_names)
        for series_name in series_names:
            grp_columns = match_columns(series_name, columns)
            # grp_columns = ["q.0", "q.1", "q.2"]
            plt.figure(figsize=(12,5))
            plt.xlabel('Frame')

            for gc in grp_columns:
                ax = df[gc].plot(grid=True, label=gc)
                h1, l1 = ax.get_legend_handles_labels()

            plt.legend(h1, l1, loc=2)
            plt.show()
