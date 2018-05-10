"""
File: dashboard.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: dashboard drawing functions.
"""

from itertools import chain
from datetime import timedelta

from bokeh import palettes
from bokeh.layouts import layout, widgetbox
from bokeh.plotting import figure
from bokeh.models import HoverTool, CustomJS, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs, Div, Select

from .draw_utils import create_box_plot


def create_benchmark_dashboard(statistics_per_problem_per_meta):
    panels = []
    for statistics_per_meta in statistics_per_problem_per_meta:
        tab_name, problem_dashboard = create_problem_dashboard(statistics_per_meta)
        panels.append(Panel(child=problem_dashboard, title=tab_name))

    dashboard = Tabs(tabs=panels)
    return dashboard


def create_problem_dashboard(statistics_per_meta):
    header = create_dashboard_header(statistics_per_meta)
    overall_comparison = create_meta_comparison(statistics_per_meta)
    #meta_dashboards = create_meta_dashboards(statistics_per_meta)

    problem_name = statistics_per_meta[0].problem.get_name()

    return problem_name, layout([[header], [overall_comparison]])


def create_dashboard_header(statistics_per_meta):
    problem_header = Div(text="""Problem Header""")
    meta_header = Div(text="""Meta Header""")
    return layout([[problem_header, meta_header]])


def create_meta_comparison(statistics_per_meta):
    # Create multiline graphs
    data_sources_fitness = []
    data_sources_time = []
    legend = []
    for i, meta_stat in enumerate(statistics_per_meta):
        runs = list(range(1, meta_stat.nb_run + 1))
        data_source_fitness = ColumnDataSource(data=dict(
            x=runs,
            y=meta_stat.best_values,
            index=runs,
            fitness=meta_stat.best_values,
        ))
        data_sources_fitness.append(data_source_fitness)
        data_source_time = ColumnDataSource(data=dict(
            x=runs,
            y=meta_stat.time_tots,
            index=runs,
            time=[str(timedelta(seconds=int(calculation_time))) for calculation_time in meta_stat.time_tots],
        ))
        data_sources_time.append(data_source_time)
        legend.append('{:d} - {}'.format(i + 1, meta_stat.metaheuristic.get_name()))

    hover_data_fitness = [('Fitness', '@fitness'), ('Run', '@index')]
    multi_graph_fitness = create_hovered_multiline_graph('Best fitness per run', 'Runs', 'Fitness',
                                                         data_sources_fitness, hover_data_fitness, legend)
    box_plot_fitness = create_box_plot('Aggregated fitness per metaheuristic', 'Fitness', legend,
                                       [data_source.data['y'] for data_source in data_sources_fitness])
    hover_data_time = [('Calculation time', '@time'), ('Run', '@index')]
    multi_graph_time = create_hovered_multiline_graph('Calculation time per run', 'Runs', 'Calculation time (in s)',
                                                      data_sources_time, hover_data_time, legend)
    box_plot_time = create_box_plot('Aggregated time per metaheuristic', 'Calculation time in s', legend,
                                       [data_source.data['y'] for data_source in data_sources_time])

    # Create header
    title = Div(text="""<span><h3>Metaheuristics comparison :</h3></span>""")
    return layout([[title], [multi_graph_fitness, multi_graph_time], [box_plot_fitness, box_plot_time]])


def create_meta_dashboards(statistics_per_meta):
    return None


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
