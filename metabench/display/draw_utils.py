"""
File: draw_utils.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: bokeh drawings utilities.
"""

import numpy as np
from bokeh.plotting import figure


def draw_best_runs_per_meta(problem, list_meta, list_statistics):
    f = figure(title="Best runs for problem {}".format(problem.__class__.__name__), y_axis_label="Fitness",
               x_axis_label="Runs")

    for i, meta in enumerate(list_meta):
        best_values = list_statistics[i].best_values
        x = range(1, len(best_values) + 1)
        f.line(x, best_values, legend=meta.__class__.__name__)
        f.circle(x, best_values, legend=meta.__class__.__name__, fill_color='white', size=8)

    return f


def draw_stats_per_meta(problem, list_meta, list_statistics):
    f = figure(title="Result per meta for problem {}".format(problem.__class__.__name__), y_axis_label="Fitness",
               x_axis_label="Meta")

    meta_names = []
    lows = []
    highs = []
    q1 = []
    q2 = []
    q3 = []

    for i, meta in enumerate(list_meta):
        meta_names.append(meta.__class__.__name__)

        best_values = list_statistics[i].best_values
        lows.append(np.amin(best_values))
        highs.append(np.amax(best_values))

        q1.append(np.percentile(best_values, 25))
        q2.append(np.percentile(best_values, 50))
        q3.append(np.percentile(best_values, 75))

    f.segment(meta_names, highs, q3, line_color='black')
    f.segment(meta_names, lows, q1, line_color='black')

    # boxes
    f.vbar(meta_names, 0.7, q2, q3, fill_color="#E08E79", line_color="black")
    f.vbar(meta_names, 0.7, q1, q2, fill_color="#3B8686", line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    f.rect(meta_names, lows, 0.2, 0.01, line_color="black")
    f.rect(meta_names, highs, 0.2, 0.01, line_color="black")

    return f
