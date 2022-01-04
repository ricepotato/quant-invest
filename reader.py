import csv
from stock import Stock
from typing import List


def reader(filepath) -> List[Stock]:
    with open(filepath, "r") as f:
        stockreader = csv.reader(f,)
        return [Stock(row[1], row[2], row[6]) for row in stockreader]

