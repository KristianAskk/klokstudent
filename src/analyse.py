from dataclasses import dataclass
import json
from typing import List

import plotly.express as px

from vinmonopolet import Vinmonopolprodukt


def main():
    with open("vinmonopol_products.json", "r", encoding="utf-8") as f:
        products = [Vinmonopolprodukt(**p) for p in json.load(f)]
        print(f"Loaded {len(products)} products from file")

    # Create a scatter plot of price per liter vs alcohol by volume
    df = {
        "name": [p.name for p in products],
        "price_per_nok": [p.alcohol_per_nok for p in products],
        "abv": [p.abv for p in products],
    }
    fig = px.scatter(df, x="abv", y="price_per_nok", text="name")
    fig.update_traces(textposition="top center")
    fig.update_layout(title="Price per liter vs alcohol by volume")
    fig.show()


if __name__ == "__main__":
    main()
