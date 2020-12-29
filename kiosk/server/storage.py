import csv
from dataclasses import dataclass, field
from datetime import datetime
from functools import reduce
from typing import List, Mapping


def _id_list_to_int(list_: List[int]) -> int:
    return reduce(lambda res, id_: res ^ (1 << id_), list_, 0)


def _int_to_id_list(int_: int) -> List[int]:
    return [id_ for id_ in range(int_.bit_length()) if int_ & (1 << id_)]


@dataclass
class StorageEntry:
    price: int
    product_ids: List[int]

    date: datetime = field(default_factory=lambda: datetime.now().replace(microsecond=0))
    deleted: bool = False


class Storage:
    # Temporary CSV-based solution

    def __init__(self, filename: str = "data.csv"):
        self._filename = filename
        self.data: List[StorageEntry] = []

        self._read()

    def _read(self):
        try:
            with open(self._filename, "r") as f:
                self.data = [
                    StorageEntry(
                        date=datetime.fromtimestamp(int(entry[0])),
                        price=int(entry[1]),
                        product_ids=_int_to_id_list(int(entry[2])),
                    )
                    for entry in csv.reader(f)
                ]
        except FileNotFoundError:
            pass  # fresh install

    def _write(self):
        with open(self._filename, "w") as f:
            csv.writer(f).writerows(
                (int(entry.date.timestamp()), entry.price, _id_list_to_int(entry.product_ids))
                for entry in self.data
                if not entry.deleted
            )

    def __delitem__(self, idx: int):
        item = self.data[idx]
        if item.deleted:
            raise IndexError()

        self.data[idx].deleted = True
        self._write()

    def append(self, price: int, product_ids: List[int]):
        self.data.append(StorageEntry(price, product_ids))
        self._write()

    def to_dict(self) -> Mapping[int, StorageEntry]:
        return {idx: entry for idx, entry in enumerate(self.data) if not entry.deleted}
