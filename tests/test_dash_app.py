import pytest
from dash import Dash
from dash.testing.application_runners import import_app


# -------------------------------------------------------
# 1. Test that the header is present
# -------------------------------------------------------
def test_header_is_present(dash_duo):
    app = import_app("dash_app")   # imports your dash_app.py
    dash_duo.start_server(app)

    header = dash_duo.find_element("h1")
    assert "Soul Foods Sales Visualiser" in header.text


# -------------------------------------------------------
# 2. Test that the visualisation (graph) is present
# -------------------------------------------------------
def test_graph_is_present(dash_duo):
    app = import_app("dash_app")
    dash_duo.start_server(app)

    graph = dash_duo.find_element("#sales_chart")
    assert graph is not None


# -------------------------------------------------------
# 3. Test that the region picker radio buttons are present
# -------------------------------------------------------
def test_region_picker_is_present(dash_duo):
    app = import_app("dash_app")
    dash_duo.start_server(app)

    region_picker = dash_duo.find_element("#region_filter")
    assert region_picker is not None

