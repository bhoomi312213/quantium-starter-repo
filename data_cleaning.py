import os
import pandas as pd

DATA_FOLDER = "data"
OUTPUT_PATH = os.path.join(DATA_FOLDER, "combined_output.csv")
PRODUCT_NAME = "pink morsel"   # product we care about

def load_and_clean(path):
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Ensure required columns exist
    required = {"product", "quantity", "price", "date", "region"}
    if not required.issubset(set(df.columns)):
        missing = required - set(df.columns)
        raise ValueError(f"Missing columns in {path}: {missing}")

    # Clean product and keep only rows matching our product
    df["product"] = df["product"].str.lower().str.strip()
    df = df[df["product"] == PRODUCT_NAME]

    # Convert quantity to int
    df["quantity"] = df["quantity"].astype(int)

    # Remove "$" from price and convert to float
    df["price"] = df["price"].replace("[\$,]", "", regex=True).astype(float)

    return df

def main():
    all_data = []

    # Loop through files in the data folder
    for file in os.listdir(DATA_FOLDER):

        # ❗ Skip the output file so we don't read it as input
        if file == "combined_output.csv":
            continue

        if file.endswith(".csv"):
            path = os.path.join(DATA_FOLDER, file)
            print(f"Processing: {path}")
            df = load_and_clean(path)
            all_data.append(df)

    # Combine all cleaned data
    combined = pd.concat(all_data, ignore_index=True)

    # Save combined output
    combined.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved combined output to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
