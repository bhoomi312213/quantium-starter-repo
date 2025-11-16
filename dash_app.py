import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# ---------------------------------------------------
# Load cleaned combined sales dataset
# ---------------------------------------------------

df = pd.read_csv("data/combined_output.csv", parse_dates=["date"])

# Ensure numeric types (some CSV values may be stored as strings)
numeric_cols = ["price", "quantity"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Create sales column
df["sales"] = df["price"] * df["quantity"]

# Remove any bad rows
df = df.dropna(subset=["sales"])

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

# Vertical line showing Pink Morsel price change
fig.add_vline(
    x="2021-01-15",
    line_width=2,
    line_dash="dash",
    annotation_text="Price Increase (15 Jan 2021)",
    annotation_position="top left"
)

# ---------------------------------------------------
# Dash App Setup
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
# Run App
# ---------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)
