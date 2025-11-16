import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# ---------------------------------------------------
# Load data
# ---------------------------------------------------
df = pd.read_csv("data/combined_output.csv", parse_dates=["date"])

# Convert numeric fields safely
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# Create sales column
df["sales"] = df["price"] * df["quantity"]

# Drop any rows where sales failed
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

# Add vertical line
fig.add_vline(
    x=pd.Timestamp("2021-01-15"),
    line_width=2,
    line_dash="dash"
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

    dcc.Graph(id="sales_chart", figure=fig)
])

# ---------------------------------------------------
# Run the server
# ---------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)

