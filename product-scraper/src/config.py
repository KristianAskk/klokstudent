import logging
import os

from dotenv import load_dotenv
from pyparsing import Optional

logging.basicConfig(level=logging.INFO)

load_dotenv()


OCPM_API_KEY = os.getenv("OCPM_API_KEY")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

PRODUCT_PAGE_URL = "https://www.vinmonopolet.no/p"

HEADERS = {
    "User-Agent": USER_AGENT,
    "Ocp-Apim-Subscription-Key": OCPM_API_KEY,
}
