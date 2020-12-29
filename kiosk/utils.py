import os
import subprocess
from typing import List

from dotenv import load_dotenv

load_dotenv()


def get_product_names() -> List[str]:
    filename = os.getenv("KIOSK_PRODUCTS")

    with open(filename, "r") as f:
        return [name.strip() for name in f.readlines()]


def get_ip_address() -> str:
    try:
        return subprocess.check_output(["hostname", "-I"], encoding="utf-8").strip()
    except OSError:
        return ""
