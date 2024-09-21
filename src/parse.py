import json
import re

import bs4
import logging

from typing import Optional

import requests

from config import HEADERS, PRODUCT_PAGE_URL
from vinmonopolet import VinmonopolProduct

logger = logging.getLogger(__name__)


def parse_product_site(product_id: str) -> Optional[VinmonopolProduct]:
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

    more_data = soup.find("main", class_="site__body")
    if more_data is None:
        logger.info(f"Could not find more data for product {product_id}")

        return None

    more_data = more_data["data-react-props"]

    json_data = json.loads(more_data)

    return VinmonopolProduct(**json_data["product"])
