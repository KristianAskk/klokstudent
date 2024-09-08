import requests
import json
from typing import Optional, List
from dataclasses import dataclass, asdict
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from parse import parse_product_site


import logging

from config import HEADERS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_products(exclude_non_drinks=True) -> List[str]:
    url = "https://apis01.vinmonopolet.no/products/v0/details-normal?start=0"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    ret = [p["basic"]["productId"] for p in data if int(p["basic"]["productId"]) > 1000]
    logger.info(f"Loaded {len(ret)} products")
    return ret


# TODO: parse schemaen i stedet for.


def main():
    product_ids = load_products()
    products = []
    total_products = len(product_ids)
    processed_count = 0

    product = product_ids[10]
    parse_product_site(product)

    # start_time = time.time()
    # with ThreadPoolExecutor(max_workers=8) as executor:
    #     future_to_id = {
    #         executor.submit(parse_product_site, product_id): product_id
    #         for product_id in product_ids
    #     }
    #
    #     for future in as_completed(future_to_id):
    #         product = future.result()
    #         if product:
    #             products.append(product)
    #             processed_count += 1
    #             print(
    #                 f"({processed_count}/{total_products}) processed product: {product.navn}"
    #             )
    #
    #         with open("vinmonopol_products.json", "w", encoding="utf-8") as f:
    #             json.dump(
    #                 [asdict(p) for p in products], f, ensure_ascii=False, indent=2
    #             )
    #
    #         time.sleep(0.08)
    #
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Time taken: {elapsed_time:.2f} seconds")
    # print(f"Total products processed: {processed_count}")


if __name__ == "__main__":
    main()
