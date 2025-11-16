import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# ---------------------------------------------------
# Load combined dataset
# ---------------------------------------------------
df = pd.read_csv("data/combined_output.csv", parse_dates=["date"])

# Create a sales column (price * quantity)
df["sales"] = df["price"] * df["quantity"]

# Sort by date
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

# Add vertical line for price change on Jan 15 2021
fig.add_vline(
    x="2021-01-15",
    line_width=2,
    line_dash="dash",
    annotation_text="Price Increase (15 Jan 2021)",
    annotation_position="top left"
)

# ---------------------------------------------------
# Dash App
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
# Run the App
# ---------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
