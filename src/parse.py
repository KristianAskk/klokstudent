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
    # find the value within the tag <script type="application/ld+json">
    json_ld_script = soup.find("script", type="application/ld+json")

    product_data = json.loads(json_ld_script.string)
    print(product_data)

    if json_ld_script is None:
        return None

    if product_data.get("brand") is None:
        return None

    alcohol_match = re.search(
        r'<strong>Alkohol</strong> <span aria-label="(\d+(?:,\d+)?) prosent">',
        response.text,
    )

    alkoholprosent = (
        float(alcohol_match.group(1).replace(",", ".")) if alcohol_match else 0.0
    )

    return Vinmonopolprodukt(**product_data, abv=alkoholprosent, product_id=product_id)
