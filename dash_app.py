import sys
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

DATA_PATH = "data/combined_output.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")


def load_and_prepare(path: str):
    """
    Loads CSV, cleans numeric columns, computes sales and returns:
      - raw_df: cleaned row-level dataframe
      - daily: dataframe aggregated by date with daily total sales
    Prints diagnostics to stdout.
    """
    try:
        # Read everything as string first to allow robust cleaning
        raw = pd.read_csv(path, dtype=str)
    except Exception as e:
        raise RuntimeError(f"Failed to read {path}: {e}")

    print(f"Loaded {len(raw)} rows from {path}")

    # Normalize column names
    raw.columns = [c.strip().lower() for c in raw.columns]

    expected = {"product", "price", "quantity", "date", "region"}
    missing = expected - set(raw.columns)
    if missing:
        raise RuntimeError(f"Missing expected columns in CSV: {missing}")

    # Trim whitespace in string columns
    raw = raw.applymap(lambda v: v.strip() if isinstance(v, str) else v)

    # Cleaning helpers: remove currency chars, commas, etc.
    def clean_numeric(s):
        s = s.fillna("").astype(str)
        # remove currency symbols, whitespace and commas, keep digits, dot and minus
        s = s.str.replace(r"[^\d\.\-]", "", regex=True)
        s = s.replace("", pd.NA)
        return pd.to_numeric(s, errors="coerce")

    # Clean numeric columns
    raw["price_clean"] = clean_numeric(raw["price"])
    raw["quantity_clean"] = clean_numeric(raw["quantity"])

    # Parse dates
    raw["date_parsed"] = pd.to_datetime(raw["date"], errors="coerce")

    # Diagnostics
    bad_price = raw[raw["price_clean"].isna() & raw["price"].notna()]
    bad_qty = raw[raw["quantity_clean"].isna() & raw["quantity"].notna()]
    bad_date = raw[raw["date_parsed"].isna() & raw["date"].notna()]

    print("Diagnostics:")
    print(f"  total rows: {len(raw)}")
    print(f"  bad price rows: {len(bad_price)}")
    if not bad_price.empty:
        print("  examples bad price values:")
        print(bad_price[["product", "price", "quantity", "date"]].head().to_string(index=False))

    print(f"  bad quantity rows: {len(bad_qty)}")
    if not bad_qty.empty:
        print("  examples bad quantity values:")
        print(bad_qty[["product", "price", "quantity", "date"]].head().to_string(index=False))

    print(f"  bad date rows: {len(bad_date)}")
    if not bad_date.empty:
        print("  examples bad date values:")
        print(bad_date[["product", "price", "quantity", "date"]].head().to_string(index=False))

    # Build usable columns and drop rows missing essentials
    raw["price"] = raw["price_clean"]
    raw["quantity"] = raw["quantity_clean"]
    raw["date"] = raw["date_parsed"]
    raw = raw.drop(columns=["price_clean", "quantity_clean", "date_parsed"], errors="ignore")

    before_drop = len(raw)
    raw = raw.dropna(subset=["price", "quantity", "date"])
    dropped = before_drop - len(raw)
    if dropped:
        print(f"Dropped {dropped} rows that lacked numeric price/quantity or valid date after cleaning.")

    # Compute sales column
    raw["sales"] = raw["price"] * raw["quantity"]

    # Aggregate to daily totals (clean time series for plotting)
    daily = raw.groupby("date", as_index=False)["sales"].sum().sort_values("date")

    print("Daily sales preview (first 8 rows):")
    print(daily.head(8).to_string(index=False))

    return raw, daily


# Load and prepare data (catch and show errors)
try:
    df_raw, daily_sales = load_and_prepare(DATA_PATH)
except Exception as e:
    # print error and prepare empty frames so the app still launches with an informative message
    print("FATAL: could not prepare data:", e, file=sys.stderr)
    df_raw = pd.DataFrame()
    daily_sales = pd.DataFrame()

# Build Plotly figure only if we have data
if daily_sales.empty:
    fig = px.line(title="No data available")
else:
    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title="Sales Over Time (daily totals)",
        labels={"date": "Date", "sales": "Sales ($)"}
    )

    # Safe vertical line (no annotation_text which can trigger timestamp mean bug)
    fig.add_vline(x=PRICE_INCREASE_DATE, line_width=2, line_dash="dash")

    # Add an explicit annotation placed at the top of the visible data (explicit y numeric)
    try:
        ymax = float(daily_sales["sales"].max())
    except Exception:
        ymax = None

    if ymax is not None:
        # place annotation slightly above the max sales value
        fig.add_annotation(
            x=PRICE_INCREASE_DATE,
            y=ymax * 1.02 if ymax > 0 else 0,
            text="Price Increase (15 Jan 2021)",
            showarrow=True,
            arrowhead=1
        )

# Build Dash app layout
app = Dash(__name__)
app.title = "Soul Foods Sales Visualiser"

if daily_sales.empty:
    app.layout = html.Div(
        [
            html.H1("Soul Foods Sales Visualiser", style={"textAlign": "center"}),
            html.P(
                "No usable sales data available after cleaning. Check the terminal output for diagnostics.",
                style={"textAlign": "center"},
            ),
            html.Pre("Terminal diagnostics were printed when the app started.", style={"whiteSpace": "pre-wrap"}),
        ],
        style={"fontFamily": "Arial, sans-serif", "maxWidth": "1000px", "margin": "0 auto", "padding": "20px"},
    )
else:
    app.layout = html.Div(
        [
            html.H1("Soul Foods Sales Visualiser", style={"textAlign": "center"}),
            html.P("Sales before and after the Pink Morsel price increase (15 Jan 2021)", style={"textAlign": "center"}),
            dcc.Graph(id="sales_chart", figure=fig),
        ],
        style={"fontFamily": "Arial, sans-serif", "maxWidth": "1000px", "margin": "0 auto", "padding": "20px"},
    )


if __name__ == "__main__":
    print("\nStarting Dash server at http://127.0.0.1:8050/ ...\n")
    app.run(debug=True)


