import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


def get_product_names() -> List[str]:
    filename = os.getenv("KIOSK_PRODUCTS")

    with open(filename, "r") as f:
        return [name.strip() for name in f.readlines()]
