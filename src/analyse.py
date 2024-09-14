from dataclasses import dataclass
import json
from typing import List

import plotly.express as px

from vinmonopolet import Vinmonopolprodukt
from systembolaget import Systembolagetprodukt


def main():
    with open("vinmonopol_products.json", "r", encoding="utf-8") as f:
        vinmonopol_products: List[Vinmonopolprodukt] = [
            Vinmonopolprodukt(**p) for p in json.load(f)
        ]
        print(f"Loaded {len(vinmonopol_products)} products from Vinmonopolet")

    vinmonopol_products = [p for p in vinmonopol_products if not p.expired]

    with open("systembolaget_products.json", "r", encoding="utf-8") as f:
        systembolaget_products: List[Systembolagetprodukt] = [
            Systembolagetprodukt(**p) for p in json.load(f)
        ]
        print(f"Loaded {len(systembolaget_products)} products from Systembolaget")

    systembolaget_products = [
        p
        for p in systembolaget_products
        if not (p.is_completely_out_of_stock or p.is_discontinued)
    ]

    df = {
        "name": [p.name for p in vinmonopol_products]
        + [p.full_name for p in systembolaget_products],
        "alcohol_per_unit": [p.alcohol_per_nok for p in vinmonopol_products]
        + [
            p.alcohol_per_sek
            for p in systembolaget_products
            if p.alcohol_per_sek is not None
        ],
        "alcohol_percentage": [p.abv for p in vinmonopol_products]
        + [
            p.alcohol_percentage
            for p in systembolaget_products
            if p.alcohol_percentage is not None
        ],
        "source": ["Vinmonopolet"] * len(vinmonopol_products)
        + ["Systembolaget"] * len(systembolaget_products),
    }

    fig = px.scatter(
        df,
        x="alcohol_percentage",
        y="alcohol_per_unit",
        color="source",
        hover_data=["name"],
        color_discrete_map={"Vinmonopolet": "red", "Systembolaget": "blue"},
    )

    fig.update_layout(
        title=f"Products from Vinmonopolet and Systembolaget - Total products: {len(vinmonopol_products) + len(systembolaget_products)}",
        xaxis_title="Alcohol percentage",
        yaxis_title="Milliliters of pure alcohol per NOK/SEK",
        hoverlabel=dict(namelength=-1),
    )

    fig.update_yaxes(tickformat=".2f")

    fig.show()


if __name__ == "__main__":
    main()
