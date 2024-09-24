from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import json
from typing import Optional, List, Any
from tqdm import tqdm
import time
import logging

from parse import parse_product_site
from config import HEADERS
from vinmonopolet import VinmonopolProduct

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_products(exclude_non_drinks=True) -> List[str]:
    url = "https://apis.vinmonopolet.no/products/v0/details-normal?start=0"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    ret = [p["basic"]["productId"] for p in data if int(p["basic"]["productId"]) > 1000]
    logger.info(f"Loaded {len(ret)} products")
    return ret


def process_single_product(product_id: str) -> Optional[VinmonopolProduct]:
    product = parse_product_site(product_id)
    if product:
        return process_object(product)
    return None


def process_object(obj: Any) -> Any:
    if isinstance(obj, str):
        return obj.encode("iso-8859-1").decode("utf-8")
    elif isinstance(obj, dict):
        return {key: process_object(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [process_object(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        for field, value in obj.__dict__.items():
            setattr(obj, field, process_object(value))
        return obj
    else:
        return obj


def process_products_multithreaded(restart=True, workers=1) -> None:
    product_ids = load_products()
    products: List[VinmonopolProduct] = []
    total_products = len(product_ids)
    start_time = time.time()

    if not restart:
        with open("vinmonopol_products.json", "r", encoding="utf-8") as f:
            products = [VinmonopolProduct(**p) for p in json.load(f)]
            logger.info(f"Loaded {len(products)} products from file")
            continuation_index = product_ids.index(products[-1].product_id)
            product_ids = product_ids[continuation_index + 1 :]

    def process_and_save(product_id: str) -> Optional[VinmonopolProduct]:
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


def process_products(restart=True) -> None:
    """Process products and save every 1000 new products fetched"""
    product_ids = load_products()
    products: List[VinmonopolProduct] = []
    total_products = len(product_ids)
    start_time = time.time()
    save_threshold = 1000
    new_products_count = 0

    if not restart:
        with open("vinmonopol_products.json", "r", encoding="utf-8") as f:
            products = [VinmonopolProduct(**p) for p in json.load(f)]
            logger.info(f"Loaded {len(products)} products from file")
            continuation_index = product_ids.index(products[-1].code)
            product_ids = product_ids[continuation_index + 1 :]

    for index, product_id in enumerate(product_ids):
        product = process_single_product(product_id)
        if product:
            logger.info(
                f"Processed product {index + 1}/{total_products}: {product.name}"
            )
            products.append(product)
            new_products_count += 1

            if new_products_count >= save_threshold:
                with open("vinmonopol_products.json", "w", encoding="utf-8") as f:
                    try:
                        json.dump(
                            [json.loads(p.model_dump_json()) for p in products],
                            f,
                            ensure_ascii=False,
                            indent=2,
                        )
                        logger.info(f"Saved {new_products_count} new products to file")
                        new_products_count = 0
                    except Exception as e:
                        logger.error(f"Failed to write to file: {e}")
                        time.sleep(10)
                        print(products[-1].model_dump_json())

    # Save any remaining products
    if new_products_count > 0:
        with open("vinmonopol_products.json", "w", encoding="utf-8") as f:
            try:
                json.dump(
                    [json.loads(p.model_dump_json()) for p in products],
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
                logger.info(f"Saved final {new_products_count} products to file")
            except Exception as e:
                logger.error(f"Failed to write to file: {e}")
                time.sleep(10)
                print(products[-1].model_dump_json())

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Processing completed. Time taken: {elapsed_time:.2f} seconds")
    logger.info(f"Total products processed: {len(products)}/{total_products}")


if __name__ == "__main__":
    process_products(restart=False)
