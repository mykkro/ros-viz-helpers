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
    if value == field:
        return value
    return None


def match_columns(field, columns):
    return list(filter(None, [match_pattern(field, c) for c in columns]))


if __name__ == "__main__":

    # Time Series plotter.

    # Example usage:
    #  python display-timeseries.py -i target/move_x.csv -f 'q.*' -f 'dq.*' -f 'tau_J.*'
    #  python display-timeseries.py -i target/move_x.csv -f 'O_T_EE.12,O_T_EE.13,O_T_EE.14' 
    #  python display-timeseries.py -i target/move_x.csv -f 'q.*' -f 'dq.*' -f 'tau_J.*' --from 100 --to 300 -o target/move_x.q.png
    #  python display-timeseries.py -i target/move_y_comp.csv -f 'ee_pos.*' -f 'ee_rot_xyzw.*' -o target/move_y.ee.png --from 100 --to 500 --plo



    cmdr = Commandr("display-timeseries", title="ROS1 bag to CSV")
    cmdr.add_argument("input", "-i", type="str", required=True)
    cmdr.add_argument("output", "-o", type="str", required=False)
    cmdr.add_argument("field", "-f|--field", nargs="*")
    cmdr.add_argument("fromframe", "--from", type='int', default=0)
    cmdr.add_argument("toframe", "--to", type='int', default=-1)
    cmdr.add_argument("plot", "--plot", type='switch')
 
    args, configs = cmdr.parse()

    input_path = args["input"]
    output_path = args["output"]
    fields = args["field"]
    from_frame = args["fromframe"]
    to_frame = args["toframe"]
    shall_plot = args["plot"]

    print(f"Input path:     {input_path}")
    print(f"Output path:    {output_path}")
    print(f"Fields:         {fields}")
    print(f"From frame:     {from_frame}")
    print(f"To frame:       {to_frame}")

    df = pd.read_csv(input_path)
    columns = df.columns

    df = df[from_frame:to_frame]

    n_groups = len(fields)
    fig, axs = plt.subplots(ncols=1, nrows=n_groups, sharex=True, figsize=(15,5*n_groups))
    if n_groups == 1:
        axs = [axs]
    plt.xlabel('Frame')

    for i, group in enumerate(fields):

        series_names = group.split(",")
        print("series names:", series_names)
        axs[i].title.set_text(group)
        axs[i].set_facecolor('#DDD')
        for series_name in series_names:
            grp_columns = match_columns(series_name, columns)
            # grp_columns = ["q.0", "q.1", "q.2"]

            for gc in grp_columns:
                df[gc].plot(grid=True, label=gc, ax=axs[i], legend=True)

    plt.tight_layout()
    if output_path is not None:
        plt.savefig(output_path)
        if shall_plot:
            plt.show()
    else:
        plt.show()
