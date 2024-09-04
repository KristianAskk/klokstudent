import requests
import json
from typing import Optional, List
from dataclasses import dataclass, asdict
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


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
    # pris_per_enhet_alkohol: Optional[float] = None

    # def __post_init__(self):
    #     self.pris_per_enhet_alkohol = self.pris / (self.alkoholprosent * self.stoerrelse_cl / 100)


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Ocp-Apim-Subscription-Key": "5fad37bb94dd4dd99e8458ee2644542d",
}


def load_products() -> List[str]:
    url = "https://apis01.vinmonopolet.no/products/v0/details-normal?start=0"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return [p["basic"]["productId"] for p in data]


# TODO: parse schemaen i stedet for.
def parse_product_site(product_id: str) -> Optional[Vinmonopolprodukt]:
    url = f"https://www.vinmonopolet.no/p/{product_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        text = response.text

        name_match = re.search(r'<h1 class="product__name">(.*?)</h1>', text)
        price_per_liter_match = re.search(
            r'<span aria-label="(\d+(?:,\d+)?) kroner og (\d+) øre per liter">', text
        )
        alcohol_match = re.search(
            r'<strong>Alkohol</strong> <span aria-label="(\d+(?:,\d+)?) prosent">', text
        )
        sugar_match = re.search(
            r'<strong>Sukker</strong> <span aria-label="(\d+(?:,\d+)?) gram per liter">',
            text,
        )
        description_match = re.search(r"<span>Smak</span><span>(.*?)</span>", text)
        size_match = re.search(
            r'<span class="amount" aria-label="(\d+) centiliter">(\d+) cl</span>', text
        )
        price_match = re.search(
            r'"offers":{"@type":"Offer","price":([\d.]+),"priceCurrency":"NOK"}', text
        )

        return Vinmonopolprodukt(
            navn=name_match.group(1) if name_match else "Unknown",
            pris_per_liter=float(price_per_liter_match.group(1).replace(",", "."))
            + float(price_per_liter_match.group(2)) / 100
            if price_per_liter_match
            else 0.0,
            alkoholprosent=float(alcohol_match.group(1).replace(",", "."))
            if alcohol_match
            else 0.0,
            produkt_id=int(product_id),
            lenke=url,
            beskrivelse=description_match.group(1)
            if description_match
            else "No description available",
            sukker_innhold=float(sugar_match.group(1).replace(",", "."))
            if sugar_match
            else 0.0,
            stoerrelse_cl=float(size_match.group(1)) if size_match else 0.0,
            pris=float(price_match.group(1)) if price_match else 0.0,
        )
    except requests.RequestException as e:
        print(f"Error fetching product {product_id}: {e}")
        return None


def main():
    product_ids = load_products()
    products = []
    total_products = len(product_ids)
    processed_count = 0

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_id = {
            executor.submit(parse_product_site, product_id): product_id
            for product_id in product_ids
        }

        for future in as_completed(future_to_id):
            product = future.result()
            if product:
                products.append(product)
                processed_count += 1
                print(
                    f"({processed_count}/{total_products}) processed product: {product.navn}"
                )

            with open("vinmonopol_products.json", "w", encoding="utf-8") as f:
                json.dump(
                    [asdict(p) for p in products], f, ensure_ascii=False, indent=2
                )

            time.sleep(0.075)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print(f"Total products processed: {processed_count}")


if __name__ == "__main__":
    main()
