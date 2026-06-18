# ================================================
#  dataset.py — Generator Dataset
# ================================================

import random


def generate_dataset(size: int, order: str = "acak") -> list:
    """
    Hasilkan dataset integer unik.

    Parameters
    ----------
    size  : 100 | 1000 | 10000
    order : 'acak' | 'terurut' | 'descending'
    """
    data = random.sample(range(1, size * 10 + 1), size)

    if order == "terurut":
        data.sort()
    elif order == "descending":
        data.sort(reverse=True)

    return data


def sample_targets(data: list, k: int = 20) -> list:
    """
    Ambil k target pencarian:
    separuh pasti ada di data, separuh kemungkinan tidak ada.
    """
    half    = k // 2
    exist   = random.sample(data, half)
    max_val = max(data) * 10
    missing = random.sample(range(max_val, max_val + k * 50), half)
    targets = exist + missing
    random.shuffle(targets)
    return targets