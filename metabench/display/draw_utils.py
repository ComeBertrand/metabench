"""
File: draw_utils.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: bokeh drawings utilities.
"""

import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot


def draw_best_runs_per_meta(list_statistics):
    if not list_statistics:
        raise ValueError("No statistics to display")

    if len(set(stats.problem for stats in list_statistics)) != 1:
        raise ValueError("All statistics must be on the same problem")

    problem = list_statistics[0].problem

    f = figure(title="Best runs for problem {}".format(problem.name), y_axis_label="Fitness",
               x_axis_label="Runs")

    for stats in list_statistics:
        x = range(1, len(stats.best_values) + 1)
        f.line(x, stats.best_values, legend=stats.metaheuristic.name)
        f.circle(x, stats.best_values, legend=stats.metaheuristic.name, fill_color='white', size=8)

    return f


def draw_stats_per_meta(list_statistics):
    if not list_statistics:
        raise ValueError("No statistics to display")

    if len(set(stats.problem for stats in list_statistics)) != 1:
        raise ValueError("All statistics must be on the same problem")

    problem = list_statistics[0].problem

    f = figure(title="Result per meta for problem {}".format(problem.name), y_axis_label="Fitness",
               x_axis_label="Meta")

    meta_names = []
    lows = []
    highs = []
    q1 = []
    q2 = []
    q3 = []

    for stats in list_statistics:
        meta_names.append(stats.metaheuristic.name)

        lows.append(np.amin(stats.best_values))
        highs.append(np.amax(stats.best_values))

        q1.append(np.percentile(stats.best_values, 25))
        q2.append(np.percentile(stats.best_values, 50))
        q3.append(np.percentile(stats.best_values, 75))

    f.segment(meta_names, highs, q3, line_color='black')
    f.segment(meta_names, lows, q1, line_color='black')

    # boxes
    f.vbar(meta_names, 0.7, q2, q3, fill_color="#E08E79", line_color="black")
    f.vbar(meta_names, 0.7, q1, q2, fill_color="#3B8686", line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    f.rect(meta_names, lows, 0.2, 0.01, line_color="black")
    f.rect(meta_names, highs, 0.2, 0.01, line_color="black")

    return f


def draw_benchmark_statistics(statistics_per_meta_and_problem_index):
    all_figures = []
    for _, stats_per_meta_index in statistics_per_meta_and_problem_index.items():
        all_meta_stats = stats_per_meta_index.values()
        all_figures.append(draw_best_runs_per_meta(all_meta_stats))
        all_figures.append(draw_stats_per_meta(all_meta_stats))

    show(gridplot(all_figures, n_cols=2))
