"""
File: draw_utils.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: bokeh drawings utilities.
"""

from itertools import chain

import numpy as np
from bokeh import palettes
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.models import HoverTool


def create_box_plot(title, y_axis_label, categories, categories_values, value_formatter=None):
    if value_formatter is None:
        value_formatter = lambda x: x

    raw_data = {
        'min': [],
        'max': [],
        'q1': [],
        'q2': [],
        'q3': [],
        'avg': [],
        'std': []
    }

    for category_values in categories_values:
        raw_data['min'].append(np.amin(category_values))
        raw_data['max'].append(np.amax(category_values))

        raw_data['q1'].append(np.percentile(category_values, 25))
        raw_data['q2'].append(np.percentile(category_values, 50))
        raw_data['q3'].append(np.percentile(category_values, 75))

        raw_data['avg'].append(np.mean(category_values))
        raw_data['std'].append(np.std(category_values))

    format_data = {}
    for key, value in raw_data.items():
        new_key = '{}_fmt'.format(key)
        format_data[new_key] = [value_formatter(item) for item in value]

    raw_data.update(format_data)
    raw_data['categories'] = categories

    data_source = ColumnDataSource(data=raw_data)

    f = figure(title=title,
               y_axis_label=y_axis_label,
               background_fill_color="#EFE8E2",
               x_range=categories)

    f.segment(categories, raw_data['max'], categories, raw_data['q3'], line_color='black')
    f.segment(categories, raw_data['min'], categories, raw_data['q1'], line_color='black')

    # boxes
    bar_high = f.vbar(x='categories', width=0.7, bottom='q2', top='q3', source=data_source, fill_color="#E08E79",
                      line_color="black")
    bar_low = f.vbar(x='categories', width=0.7, bottom='q1', top='q2', source=data_source, fill_color="#3B8686",
                     line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    whiskers_height = min([raw_data['max'][i] - raw_data['min'][i] for i in range(len(raw_data['max']))]) / 1000
    f.rect(categories, raw_data['min'], 0.2, whiskers_height, line_color="black")
    f.rect(categories, raw_data['max'], 0.2, whiskers_height, line_color="black")

    hover = HoverTool(tooltips=[('Max', '@max_fmt'), ('3td Quartile', '@q3_fmt'), ('Median', '@q2_fmt'),
                                ('1st Quartile', '@q1_fmt'), ('Min', '@min_fmt'), ('Avg', '@avg_fmt'), ('Std', '@std_fmt')],
                      renderers=[bar_high, bar_low])
    f.add_tools(hover)

    f.xgrid.grid_line_color = None
    f.ygrid.grid_line_color = "white"
    f.grid.grid_line_width = 2
    f.xaxis.major_label_text_font_size="12pt"

    return f



def create_hovered_multiline_graph(title, x_axis_label, y_axis_label, data_sources, hover_data, legend):
    f = figure(title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label)

    nb_lines = len(data_sources)
    colors = get_colors(nb_lines)

    circle_glyphs = []
    for i, data_source in enumerate(data_sources):
        item_kwargs = {'line_color': colors[i]}
        if legend:
            item_kwargs['legend'] = legend[i]

        f.line('x', 'y', source=data_source, **item_kwargs)
        circle_glyphs.append(f.circle('x', 'y', source=data_source, fill_color='white', size=8, **item_kwargs))

    # Hover only on the circles
    hover = HoverTool(renderers=circle_glyphs, tooltips=hover_data, mode='vline')
    f.add_tools(hover)
    f.legend.click_policy = 'hide'

    return f


def create_hovered_single_line_graph(title, x_axis_label, y_axis_label, data_source, hover_data):
    hover = HoverTool(tooltips=hover_data, mode='vline')
    f = figure(title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
    f.add_tools(hover)

    color = get_colors(1)[0]

    f.line('x', 'y', source=data_source, line_color=color)

    return f


def get_colors(nb_lines):
    colors = []
    nb_palette = nb_lines // 20
    colors = [color for color in chain(nb_palette * palettes.d3['Category20'][20])]
    remaining = nb_lines % 20
    if remaining <= 2:
        colors += palettes.d3['Category10'][3]
    elif remaining <= 10:
        colors += palettes.d3['Category10'][len(y_values_per_line)]
    elif remaining <= 20:
        colors += palettes.d3['Category20'][len(y_values_per_line)]

    return colors
