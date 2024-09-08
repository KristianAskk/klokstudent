import requests
import json
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import logging
from tqdm import tqdm

from parse import parse_product_site
from config import HEADERS
from Vinmonopolprodukt import Vinmonopolprodukt

logger = logging.getLogger(__name__)
# no logging whatsoever
logger.setLevel(logging.CRITICAL)


def load_products(exclude_non_drinks=True) -> List[str]:
    url = "https://apis01.vinmonopolet.no/products/v0/details-normal?start=0"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    ret = [p["basic"]["productId"] for p in data if int(p["basic"]["productId"]) > 1000]
    logger.info(f"Loaded {len(ret)} products")
    return ret


def process_single_product(product_id: str) -> Optional[Vinmonopolprodukt]:
    product = parse_product_site(product_id)
    if product:
        for field, value in product.__dict__.items():
            if isinstance(value, str):
                setattr(product, field, value.encode("iso-8859-1").decode("utf-8"))
    return product


def process_products(restart=True, workers=1) -> None:
    product_ids = load_products()
    products: List[Vinmonopolprodukt] = []
    total_products = len(product_ids)
    start_time = time.time()

    if not restart:
        with open("vinmonopol_products.json", "r", encoding="utf-8") as f:
            products = [Vinmonopolprodukt(**p) for p in json.load(f)]
            logger.info(f"Loaded {len(products)} products from file")
            continuation_index = product_ids.index(products[-1].product_id)
            product_ids = product_ids[continuation_index + 1 :]

    def process_and_save(product_id: str) -> Optional[Vinmonopolprodukt]:
        product = process_single_product(product_id)
        if product:
            logger.info(f"Processed product: {product.name}")
        return product

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(process_and_save, product_id) for product_id in product_ids
        ]

        for future in tqdm(
            as_completed(futures), total=len(product_ids), desc="Processing products"
        ):
            product = future.result()
            if product:
                products.append(product)

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
                        print(products[-1].model_dump_json())

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    process_products(restart=True, workers=4)
