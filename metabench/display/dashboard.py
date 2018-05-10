"""
File: dashboard.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: dashboard drawing functions.
"""

from datetime import timedelta

from bokeh.layouts import layout, column
from bokeh.models import ColumnDataSource, CustomJS, Panel, Tabs, Div, Slider

from .draw_utils import create_box_plot, create_hovered_multiline_graph, create_hovered_single_line_graph


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
    meta_dashboards = create_meta_dashboards(statistics_per_meta)

    problem_name = statistics_per_meta[0].problem.get_name()

    return problem_name, layout([[header], [overall_comparison], [meta_dashboards]])


def create_dashboard_header(statistics_per_meta):
    problem_header = Div(text="""Problem Header""")
    meta_header = Div(text="""Meta Header""")
    return layout([[problem_header, meta_header]])


def create_meta_comparison(statistics_per_meta):
    # Create multiline graphs
    data_sources_fitness = []
    data_sources_time = []
    legend = []

    fitness_formatter = lambda x: "{:.1e}".format(x)
    time_formatter = lambda x: str(timedelta(seconds=int(x)))

    for i, meta_stat in enumerate(statistics_per_meta):
        runs = list(range(1, meta_stat.nb_run + 1))
        data_source_fitness = ColumnDataSource(data=dict(
            x=runs,
            y=meta_stat.best_values,
            index=runs,
            fitness=[fitness_formatter(fitness) for fitness in meta_stat.best_values],
        ))
        data_sources_fitness.append(data_source_fitness)
        data_source_time = ColumnDataSource(data=dict(
            x=runs,
            y=meta_stat.time_tots,
            index=runs,
            time=[time_formatter(calculation_time) for calculation_time in meta_stat.time_tots],
        ))
        data_sources_time.append(data_source_time)
        legend.append('{:d} - {}'.format(i + 1, meta_stat.metaheuristic.get_name()))

    hover_data_fitness = [('Fitness', '@fitness'), ('Run', '@index')]
    multi_graph_fitness = create_hovered_multiline_graph('Best fitness per run', 'Runs', 'Fitness',
                                                         data_sources_fitness, hover_data_fitness, legend)
    box_plot_fitness = create_box_plot('Aggregated fitness per metaheuristic', 'Fitness', legend,
                                       [data_source.data['y'] for data_source in data_sources_fitness],
                                       value_formatter=fitness_formatter)

    hover_data_time = [('Calculation time', '@time'), ('Run', '@index')]
    multi_graph_time = create_hovered_multiline_graph('Calculation time per run', 'Runs', 'Calculation time (in s)',
                                                      data_sources_time, hover_data_time, legend)
    box_plot_time = create_box_plot('Aggregated time per metaheuristic', 'Calculation time in s', legend,
                                    [data_source.data['y'] for data_source in data_sources_time],
                                    value_formatter=time_formatter)

    # Create header
    title = Div(text="""</br></br><span><h3>Metaheuristics comparison :</h3></span>""")
    return layout([[title], [multi_graph_fitness, multi_graph_time], [box_plot_fitness, box_plot_time]])


def create_meta_dashboards(statistics_per_meta):
    panels = []
    for i, meta_stat in enumerate(statistics_per_meta):
        tab_name = '{:d} - {}'.format(i + 1, meta_stat.metaheuristic.get_name())
        meta_dashboard = create_meta_dashboard(meta_stat)
        panels.append(Panel(child=meta_dashboard, title=tab_name))

    dashboard = Tabs(tabs=panels)

    # Create header
    title = Div(text="""</br></br><span><h3>Metaheuristics analysis :</h3></span>""")
    return layout([[title], [dashboard]])


def create_meta_dashboard(meta_stat):
    values_per_run = {}
    for i in range(meta_stat.nb_run):
        values_per_run['values_{:d}'.format(i+1)] = meta_stat.get_run_values(i)
        values_per_run['iter_{:d}'.format(i+1)] = list(range(meta_stat.get_run_nb_iterations(i)))

    all_data_source = ColumnDataSource(data=values_per_run)

    data_source_fitness = ColumnDataSource(data=dict(
        x=values_per_run['iter_1'],
        y=values_per_run['values_1']
    ))

    graph_fitness_per_iter = create_hovered_single_line_graph('Best fitness evolution during iterations', 'Iterations',
                                                              'Fitness', data_source_fitness,
                                                              [('Value', '@y'), ('Iteration', '@x')])

    slider_callback = CustomJS(args=dict(source=data_source_fitness, all_data_source=all_data_source), code="""
        var data = source.data;
        var f = cb_obj.value;
        var all_data = all_data_source.data;
        data['x'] = all_data['iter_' + f];
        data['y'] = all_data['values_' + f];
        source.trigger('change');
    """)
    slider = Slider(start=1, end=meta_stat.nb_run, value=1, step=1, title="Run nb")
    slider.js_on_change('value', slider_callback)

    return column(slider, graph_fitness_per_iter)
