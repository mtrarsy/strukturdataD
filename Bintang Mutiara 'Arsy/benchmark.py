# ================================================
#  benchmark.py — Pengukur Waktu Eksekusi
# ================================================

import time
from structures import ArrayDS, BST, HashTable, AVLTree
from dataset    import sample_targets

REPEAT = 3   # jumlah pengulangan untuk rata-rata


def _ms(fn) -> float:
    """Jalankan fn() dan kembalikan durasi dalam milidetik."""
    start = time.perf_counter()
    fn()
    return (time.perf_counter() - start) * 1000


def _build(data: list):
    """Bangun keempat struktur data dari data yang sama."""
    arr = ArrayDS()
    bst = BST()
    ht  = HashTable()
    avl = AVLTree()
    for v in data:
        arr.insert(v)
        bst.insert(v)
        ht.insert(v)
        avl.insert(v)
    return arr, bst, ht, avl


# ── INSERT ──────────────────────────────────────
def bench_insert(data: list) -> dict:
    results = {}

    for name, DSClass in [("Array", ArrayDS), ("BST", BST),
                          ("Hash Table", HashTable), ("AVL Tree", AVLTree)]:
        def _fn(C=DSClass):
            ds = C()
            for v in data:
                ds.insert(v)
        times = [_ms(_fn) for _ in range(REPEAT)]
        results[name] = round(sum(times) / REPEAT, 4)

    return results


# ── SEARCH ──────────────────────────────────────
def bench_search(data: list, targets: list) -> dict:
    arr, bst, ht, avl = _build(data)
    results = {}

    for name, ds in [("Array", arr), ("BST", bst),
                     ("Hash Table", ht), ("AVL Tree", avl)]:
        def _fn(d=ds):
            for t in targets:
                d.search(t)
        times = [_ms(_fn) for _ in range(REPEAT)]
        results[name] = round(sum(times) / REPEAT, 6)

    return results


# ── DELETE ──────────────────────────────────────
def bench_delete(data: list, targets: list) -> dict:
    results = {}

    for name, DSClass in [("Array", ArrayDS), ("BST", BST),
                          ("Hash Table", HashTable), ("AVL Tree", AVLTree)]:
        ds = DSClass()
        for v in data:
            ds.insert(v)
        def _fn(d=ds):
            for t in targets:
                d.delete(t)
        times = [_ms(_fn) for _ in range(REPEAT)]
        results[name] = round(sum(times) / REPEAT, 4)

    return results


# ── FULL BENCHMARK ──────────────────────────────
def run_full_benchmark(data: list) -> dict:
    targets = sample_targets(data, k=20)
    return {
        "insert": bench_insert(data),
        "search": bench_search(data, targets),
        "delete": bench_delete(data, targets),
    }