import json
import re

import bs4

from typing import Optional

import requests

from config import HEADERS, PRODUCT_PAGE_URL
from Vinmonopolprodukt import Vinmonopolprodukt


def parse_product_site(product_id: str) -> Optional[Vinmonopolprodukt]:
    url = f"{PRODUCT_PAGE_URL}/{product_id}"
    response = requests.get(url, headers=HEADERS)

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # find the value within the tag <script type="application/ld+json">
    json_ld_script = soup.find("script", type="application/ld+json")

    if json_ld_script is None:
        return None

    alcohol_match = re.search(
        r'<strong>Alkohol</strong> <span aria-label="(\d+(?:,\d+)?) prosent">',
        response.text,
    )

    alkoholprosent = (
        float(alcohol_match.group(1).replace(",", ".")) if alcohol_match else 0.0
    )

    product_data = json.loads(json_ld_script.string)

    return Vinmonopolprodukt(**product_data, abv=alkoholprosent)
