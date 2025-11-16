import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import dash_app  # <-- direct import of your Dash file


@pytest.fixture
def app_runner():
    return dash_app.app   # <-- return the Dash app object


def test_header_present(dash_duo, app_runner):
    dash_duo.start_server(app_runner)
    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Soul Foods Sales Visualiser" in header.text


def test_visualisation_present(dash_duo, app_runner):
    dash_duo.start_server(app_runner)
    graph = dash_duo.find_element("#sales_chart")
    assert graph is not None
    dash_duo.wait_for_element(".js-plotly-plot")


def test_region_picker_present(dash_duo, app_runner):
    dash_duo.start_server(app_runner)
    picker = dash_duo.find_element("#region_filter")
    assert picker is not None
    labels = dash_duo.find_elements("#region_filter label")
    assert len(labels) >= 4
