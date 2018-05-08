"""
File: dashboard.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: dashboard drawing functions.
"""

from bokeh.layouts import layout
from bokeh.models.widgets import Panel, Tabs, Div


def create_benchmark_dashboard(statistics_per_problem_per_meta):
    panels = []
    for statistics_per_meta in statistics_per_problem_per_meta:
        tab_name, problem_dashboard = create_problem_dashboard(statistics_per_meta)
        panels.append(Panel(child=problem_dashboard, title=tab_name))

    dashboard = Tabs(tabs=panels)
    return layout([[Tabs]], sizing_mode='scale_width')


def create_problem_dashboard(statistics_per_meta):
    header = create_dashboard_header(statistics_per_meta)
    overall_comparison = create_meta_comparison(statistics_per_meta)
    meta_dashboards = create_meta_dashboards(statistics_per_meta)

    problem_name = statistics_per_meta[0].problem.get_name()

    return problem_name, layout([[header], [overall_comparison], [meta_dashboards]], sizing_mode='scale_width')


def create_dashboard_header(statistics_per_meta):
    problem_header = Div(text="""Problem Header""")
    meta_header = Div(text="""Meta Header""")
    return layout([[problem_header, meta_header]], sizing_mode='scale_width')


def create_meta_comparison(statistics_per_meta):
    return None


def create_meta_dashboards(statistics_per_meta):
    return None
