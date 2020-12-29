import csv
import datetime
from typing import List


class Storage:
    # Temporary CSV-based solution

    def __init__(self, filename: str = "data.csv"):
        self._filename = filename
        self.data = []

        self._read()

    def _read(self):
        try:
            with open(self._filename, "r") as f:
                self.data = list(csv.reader(f))
        except FileNotFoundError:
            pass  # fresh install

    def _write(self):
        with open(self._filename, "w") as f:
            csv.writer(f).writerows(self.data)

    def append(self, price: int, product_ids: List[int]):
        timestamp = int(datetime.datetime.now().timestamp())

        self.data.append((timestamp, price, product_ids))
        self._write()
