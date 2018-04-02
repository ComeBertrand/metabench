"""
File: draw_utils.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: bokeh drawings utilities.
"""

import numpy as np
from bokeh import palettes
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot


def create_multiline_graph(title, y_axis_label, x_axis_label, x_range, y_values_per_line, y_labels):
    f = figure(title=title, y_axis_label=y_axis_label, x_axis_label=x_axis_label)

    colors = []
    if len(y_values_per_line) <= 2:
        colors = palettes.d3['Category10'][3]
    elif len(y_values_per_line) <= 10:
        colors = palettes.d3['Category10'][len(y_values_per_line)]
    elif len(y_values_per_line) <= 20:
        colors = palettes.d3['Category20'][len(y_values_per_line)]
    # TODO: Handle more than 20 categories

    for i, y_values in enumerate(y_values_per_line):
        f.line(x_range, y_values, legend=y_labels[i], line_color=colors[i])
        f.circle(x_range, y_values, legend=y_labels[i], line_color=colors[i],
                 fill_color='white', size=8)

    return f


def create_box_plot(title, y_axis_label, categories, categories_values):
    meta_names = []
    lows = []
    highs = []
    q1 = []
    q2 = []
    q3 = []

    for category_values in categories_values:
        lows.append(np.amin(category_values))
        highs.append(np.amax(category_values))

        q1.append(np.percentile(category_values, 25))
        q2.append(np.percentile(category_values, 50))
        q3.append(np.percentile(category_values, 75))

    f = figure(title=title,
               y_axis_label=y_axis_label,
               background_fill_color="#EFE8E2",
               x_range=categories)

    f.segment(categories, highs, categories, q3, line_color='black')
    f.segment(categories, lows, categories, q1, line_color='black')

    # boxes
    f.vbar(categories, 0.7, q2, q3, fill_color="#E08E79", line_color="black")
    f.vbar(categories, 0.7, q1, q2, fill_color="#3B8686", line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    whiskers_height = min([q3[i] - q1[i] for i in range(len(q3))]) / 1000
    f.rect(categories, lows, 0.2, whiskers_height, line_color="black")
    f.rect(categories, highs, 0.2, whiskers_height, line_color="black")

    f.xgrid.grid_line_color = None
    f.ygrid.grid_line_color = "white"
    f.grid.grid_line_width = 2
    f.xaxis.major_label_text_font_size="12pt"

    return f


def draw_best_values_per_meta(list_statistics):
    if not list_statistics:
        raise ValueError("No statistics to display")

    if len(set(stats.problem for stats in list_statistics)) != 1:
        raise ValueError("All statistics must be on the same problem")

    problem = list_statistics[0].problem
    title = "Best runs for problem {}".format(problem.get_name())
    y_axis_label = "Fitness"
    x_axis_label = "Runs"
    x_range = range(1, len(list_statistics[0].best_values) + 1)

    y_labels = ["{}-{:d}".format(stats.metaheuristic.get_name(), i) for i, stats in enumerate(list_statistics)]
    best_values_per_meta = [stats.best_values for stats in list_statistics]

    return (create_multiline_graph(title, y_axis_label, x_axis_label, x_range, best_values_per_meta, y_labels),
            create_box_plot(title, y_axis_label, y_labels, best_values_per_meta))


def draw_time_per_run_per_meta(list_statistics):
    if not list_statistics:
        raise ValueError("No statistics to display")

    if len(set(stats.problem for stats in list_statistics)) != 1:
        raise ValueError("All statistics must be on the same problem")

    problem = list_statistics[0].problem

    title = "Time per run for problem {}".format(problem.get_name())
    y_axis_label = "Computation time (in s)"
    x_axis_label = "Runs"

    x_range = range(1, len(list_statistics[0].time_tots) + 1)
    y_labels = ["{}-{:d}".format(stats.metaheuristic.get_name(), i) for i, stats in enumerate(list_statistics)]

    times_run_per_meta = [stats.time_tots for stats in list_statistics]

    return (create_multiline_graph(title, y_axis_label, x_axis_label, x_range, times_run_per_meta, y_labels),
            create_box_plot(title, y_axis_label, y_labels, times_run_per_meta))


def draw_nb_iteration_per_meta(list_statistics):
    if not list_statistics:
        raise ValueError("No statistics to display")

    if len(set(stats.problem for stats in list_statistics)) != 1:
        raise ValueError("All statistics must be on the same problem")

    problem = list_statistics[0].problem

    title = "Nb of iteration for problem {}".format(problem.get_name())
    y_axis_label = "Nb iterations"
    x_axis_label = "Runs"

    x_range = range(1, len(list_statistics[0].nb_iter_per_run) + 1)
    y_labels = ["{}-{:d}".format(stats.metaheuristic.get_name(), i) for i, stats in enumerate(list_statistics)]

    nb_run_per_meta = [stats.nb_iter_per_run for stats in list_statistics]

    return (create_multiline_graph(title, y_axis_label, x_axis_label, x_range, nb_run_per_meta, y_labels),
            create_box_plot(title, y_axis_label, y_labels, nb_run_per_meta))


def draw_benchmark_statistics(statistics_per_meta_and_problem_index):
    all_figures = []
    for _, stats_per_meta_index in statistics_per_meta_and_problem_index.items():
        # TODO: create a numpy array and remove for loop from above functions
        all_meta_stats = list(stats_per_meta_index.values())
        for func in [draw_best_values_per_meta, draw_time_per_run_per_meta, draw_nb_iteration_per_meta]:
            line_figure, box_figure = func(all_meta_stats)
            all_figures.append(line_figure)
            all_figures.append(box_figure)

    show(gridplot(all_figures, ncols=2))
