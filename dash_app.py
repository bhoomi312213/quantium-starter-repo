import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# --------------------------------------------------------
# Load and prepare data
# --------------------------------------------------------
df = pd.read_csv("data/combined_output.csv", parse_dates=["date"])

# Clean columns
df["price"] = df["price"].astype(float)
df["quantity"] = df["quantity"].astype(int)

# Create sales column
df["sales"] = df["price"] * df["quantity"]

# Sort data by date
df = df.sort_values("date")

# --------------------------------------------------------
# Initialise Dash app
# --------------------------------------------------------
app = Dash(__name__)
app.title = "Soul Foods Sales Visualiser"

# --------------------------------------------------------
# Layout
# --------------------------------------------------------
app.layout = html.Div(
    style={
        "font-family": "Arial",
        "padding": "20px",
        "background-color": "#F9FAFB",
    },
    children=[
        html.H1(
            "Soul Foods Sales Visualiser",
            style={
                "textAlign": "center",
                "color": "#333333",
                "marginBottom": "10px",
            },
        ),

        html.P(
            "Explore Pink Morsel sales by region before and after the price increase.",
            style={"textAlign": "center", "color": "#555555"},
        ),

        html.Div(
            style={
                "width": "40%",
                "margin": "20px auto",
                "padding": "10px",
                "background": "white",
                "borderRadius": "8px",
                "boxShadow": "0px 0px 6px rgba(0,0,0,0.1)",
            },
            children=[
                html.Label("Select Region:", style={"fontWeight": "bold"}),
                dcc.RadioItems(
                    id="region_filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    labelStyle={"display": "block", "padding": "4px"},
                    inputStyle={"marginRight": "6px"},
                ),
            ],
        ),

        dcc.Graph(id="sales_chart"),
    ],
)

# --------------------------------------------------------
# Callbacks
# --------------------------------------------------------
@app.callback(
    Output("sales_chart", "figure"),
    Input("region_filter", "value"),
)
def update_chart(selected_region):

    # Filter region
    if selected_region == "all":
        dff = df.copy()
    else:
        dff = df[df["region"] == selected_region]

    # Create line chart
    fig = px.line(
        dff,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales — Region: {selected_region.title()}",
        labels={"date": "Date", "sales": "Sales ($)"},
    )

    # Add safe vline (no annotation to avoid timestamp error)
    fig.add_vline(
        x=pd.Timestamp("2021-01-15"),
        line_width=2,
        line_dash="dash",
        line_color="red",
    )

    # Manual annotation (safe for timestamps)
    fig.add_annotation(
        x=pd.Timestamp("2021-01-15"),
        y=dff["sales"].max() if len(dff) else 0,
        text="Price Increase",
        showarrow=True,
        arrowhead=1,
        font=dict(color="red"),
    )

    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="#F9FAFB",
    )

    return fig

# --------------------------------------------------------
# Run app
# --------------------------------------------------------
if __name__ == "__main__":
    print("\nDash running at http://127.0.0.1:8050/\n")
    app.run(debug=True)



