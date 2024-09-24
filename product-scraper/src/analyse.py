from dataclasses import dataclass
import json
from typing import List, Dict, Any

import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

from vinmonopolet import Vinmonopolprodukt
from systembolaget import Systembolagetprodukt


def load_data() -> Dict[str, List[Any]]:
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

    return {
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


def perform_regression_analysis(
    df: Dict[str, List[Any]]
) -> Dict[str, Dict[str, float]]:
    results = {}
    for source in ["Vinmonopolet", "Systembolaget"]:
        mask = np.array(df["source"]) == source
        X = np.array(df["alcohol_percentage"])[mask].reshape(-1, 1)
        y = np.array(df["alcohol_per_unit"])[mask]

        model = LinearRegression()
        model.fit(X, y)

        results[source] = {
            "slope": model.coef_[0],
            "intercept": model.intercept_,
            "r_squared": model.score(X, y),
        }

    return results


def create_scatter_plot(
    df: Dict[str, List[Any]], regression_results: Dict[str, Dict[str, float]]
):
    fig = px.scatter(
        df,
        x="alcohol_percentage",
        y="alcohol_per_unit",
        color="source",
        hover_data=["name"],
        color_discrete_map={"Vinmonopolet": "red", "Systembolaget": "blue"},
    )

    for source, color in [("Vinmonopolet", "red"), ("Systembolaget", "blue")]:
        mask = np.array(df["source"]) == source
        x = np.array(df["alcohol_percentage"])[mask]
        y = np.array(df["alcohol_per_unit"])[mask]

        slope = regression_results[source]["slope"]
        intercept = regression_results[source]["intercept"]
        r_squared = regression_results[source]["r_squared"]

        x_range = np.linspace(min(x), max(x), 100)
        y_pred = slope * x_range + intercept

        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=y_pred,
                mode="lines",
                name=f"{source} Regression (R² = {r_squared:.3f})",
                line=dict(color=color, dash="dash"),
            )
        )

    fig.update_layout(
        title=f"Products from Vinmonopolet and Systembolaget - Total products: {len(df['name'])}",
        xaxis_title="Alcohol percentage",
        yaxis_title="Milliliters of pure alcohol per NOK/SEK",
        hoverlabel=dict(namelength=-1),
    )

    fig.update_yaxes(tickformat=".2f")

    return fig


def main():
    df = load_data()
    regression_results = perform_regression_analysis(df)
    fig = create_scatter_plot(df, regression_results)
    fig.show()

    print("Regression Analysis Results:")
    for source, results in regression_results.items():
        print(f"\n{source}:")
        print(f"  Slope: {results['slope']:.4f}")
        print(f"  Intercept: {results['intercept']:.4f}")
        print(f"  R-squared: {results['r_squared']:.4f}")


if __name__ == "__main__":
    main()
