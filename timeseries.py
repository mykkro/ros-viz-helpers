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


def timeseriesplot(input_path, output_path, fields, from_frame, to_frame, shall_plot):

    df = pd.read_csv(input_path)
    columns = df.columns

    df = df[from_frame:to_frame]
    print(f"[{from_frame}:{to_frame}]")
    n_groups = len(fields)
    fig, axs = plt.subplots(ncols=1, nrows=n_groups, sharex=True, figsize=(15,5*n_groups))
    fig.suptitle(input_path + f" [{';'.join(fields)}]", fontsize=12)
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
