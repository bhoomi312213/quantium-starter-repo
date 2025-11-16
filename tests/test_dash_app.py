import pytest
from dash.testing.application_runners import import_app


@pytest.fixture
def app_runner():
    # Load the Dash app from dash_app.py (file you provided)
    return import_app("dash_app")


def test_header_present(dash_duo, app_runner):
    dash_duo.start_server(app_runner)

    # There is no header ID, so locate <h1>
    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Soul Foods Sales Visualiser" in header.text


def test_visualisation_present(dash_duo, app_runner):
    dash_duo.start_server(app_runner)

    # Graph exists
    graph = dash_duo.find_element("#sales_chart")
    assert graph is not None

    # Ensure Plotly actually loads
    dash_duo.wait_for_element(".js-plotly-plot")


def test_region_picker_present(dash_duo, app_runner):
    dash_duo.start_server(app_runner)

    # RadioItems ID from your file
    picker = dash_duo.find_element("#region_filter")
    assert picker is not None

    # Ensure the radio options exist
    # (dash renders them as <label> wrappers)
    labels = dash_duo.find_elements("#region_filter label")
    assert len(labels) >= 4


