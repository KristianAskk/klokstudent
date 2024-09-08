import requests
import json
from typing import Optional, List
from dataclasses import dataclass, asdict
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

import ast
from parse import parse_product_site


import logging

from config import HEADERS

from Vinmonopolprodukt import Vinmonopolprodukt

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_products(exclude_non_drinks=True) -> List[str]:
    url = "https://apis01.vinmonopolet.no/products/v0/details-normal?start=0"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    ret = [p["basic"]["productId"] for p in data if int(p["basic"]["productId"]) > 1000]
    logger.info(f"Loaded {len(ret)} products")
    return ret


def process_products() -> None:
    product_ids = load_products()
    products: List[Vinmonopolprodukt] = []
    total_products = len(product_ids)
    processed_count = 0

    start_time = time.time()
    for product_id in product_ids:
        product = parse_product_site(product_id)
        if product:
            # Ensure all string fields are properly decoded
            for field, value in product.__dict__.items():
                if isinstance(value, str):
                    setattr(product, field, value.encode("iso-8859-1").decode("utf-8"))

            products.append(product)
            processed_count += 1
            logging.info(
                f"({processed_count}/{total_products}) processed product: {product.name}"
            )

            with open("vinmonopol_products.json", "w", encoding="utf-8") as f:
                try:
                    json.dump(
                        [json.loads(p.model_dump_json()) for p in products],
                        f,
                        ensure_ascii=False,
                        indent=2,
                    )
                except Exception as e:
                    logger.error(f"Failed to write to file: {e}")
                    time.sleep(10)
                    # Print the value of what couldn't be parsed
                    print(products[-1].model_dump_json())

        time.sleep(0.09)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    process_products()
