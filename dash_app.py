import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# ---------------------------------------------------
# Load cleaned combined sales dataset (from Task 1)
# ---------------------------------------------------
df = pd.read_csv("data/combined_output.csv", parse_dates=["date"])

# Sort by date (required)
df = df.sort_values("date")

# ---------------------------------------------------
# Create line chart
# ---------------------------------------------------
fig = px.line(
    df,
    x="date",
    y="sales",
    title="Sales Over Time",
    labels={"date": "Date", "sales": "Sales ($)"}
)

# Vertical line for Pink Morsel price change
fig.add_vline(
    x="2021-01-15",
    line_width=2,
    line_dash="dash",
    annotation_text="Price Increase (15 Jan 2021)"
)

# ---------------------------------------------------
# Dash App Layout
# ---------------------------------------------------
app = Dash(__name__)
app.title = "Soul Foods Sales Visualiser"

app.layout = html.Div([
    html.H1(
        "Soul Foods Sales Visualiser",
        style={"textAlign": "center"}
    ),

    html.P(
        "Sales before and after the Pink Morsel price increase (15 Jan 2021)",
        style={"textAlign": "center"}
    ),

    dcc.Graph(
        id="sales_chart",
        figure=fig
    )
])

# ---------------------------------------------------
# Run the server
# ---------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)

