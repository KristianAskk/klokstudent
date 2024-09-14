import json
import re

import bs4

from typing import Optional

import requests

from config import HEADERS, PRODUCT_PAGE_URL
from vinmonopolet import Vinmonopolprodukt


def parse_product_site(product_id: str) -> Optional[Vinmonopolprodukt]:
    url = f"{PRODUCT_PAGE_URL}/{product_id}"
    response = requests.get(url, headers=HEADERS)

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    json_ld_script = soup.find("script", type="application/ld+json")

    if json_ld_script is None:
        return None

    product_data = json.loads(json_ld_script.string)

    if product_data.get("brand") is None:
        return None

    print(product_data)
    expired = True if soup.find("div", class_="product-price-expired") else False

    alcohol_match = re.search(
        r'<strong>Alkohol</strong> <span aria-label="(\d+(?:,\d+)?) prosent">',
        response.text,
    )

    alkoholprosent = (
        float(alcohol_match.group(1).replace(",", ".")) if alcohol_match else 0.0
    )

    return Vinmonopolprodukt(
        **product_data, abv=alkoholprosent, product_id=product_id, expired=expired
    )
