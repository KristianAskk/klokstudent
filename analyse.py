from dataclasses import dataclass
import json
from typing import List


@dataclass
class Vinmonopolprodukt:
    navn: str
    pris_per_liter: float
    alkoholprosent: float
    produkt_id: int
    lenke: str
    beskrivelse: str
    sukker_innhold: float
    stoerrelse_cl: float
    pris: float


def load_products(filename: str) -> List[Vinmonopolprodukt]:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Vinmonopolprodukt(**product) for product in data]


def calculate_alcohol_per_krone(product: Vinmonopolprodukt) -> float:
    liters = product.stoerrelse_cl / 100
    total_alcohol = liters * (product.alkoholprosent / 100)
    return total_alcohol / product.pris if product.pris > 0 else 0


def find_top_value_products(
    products: List[Vinmonopolprodukt], top_n: int = 30
) -> List[Vinmonopolprodukt]:
    return sorted(products, key=calculate_alcohol_per_krone, reverse=True)[:top_n]


def main():
    products = load_products("vinmonopol_products.json")
    top_products = find_top_value_products(products)

    print(f"Top 10 products with the most alcohol per krone:")
    for i, product in enumerate(top_products, 1):
        alcohol_per_krone = calculate_alcohol_per_krone(product)
        print(f"\n{i}. {product.navn}")
        print(f"   Product ID: {product.produkt_id}")
        print(f"   Price: {product.pris:.2f} NOK")
        print(f"   Volume: {product.stoerrelse_cl} cl")
        print(f"   Alcohol percentage: {product.alkoholprosent:.1f}%")
        print(
            f"   Alcohol per krone: {alcohol_per_krone:.6f} liters of pure alcohol per NOK"
        )
        print(f"   Link: {product.lenke}")


if __name__ == "__main__":
    main()
