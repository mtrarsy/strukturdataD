import time
import random
import sys

# Meningkatkan limit rekursi untuk dataset besar (khususnya untuk Quick Sort)
sys.setrecursionlimit(200000)

# --- Implementasi Algoritma ---

def bubble_sort(arr):
    n = len(arr)
    arr_copy = arr.copy()
    for i in range(n):
        for j in range(0, n-i-1):
            if arr_copy[j] > arr_copy[j+1]:
                arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
    return arr_copy

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# --- Fungsi Benchmarking ---

def benchmark():
    data_sizes = [100, 1000, 10000, 50000]
    algorithms = [("Bubble Sort", bubble_sort), ("Merge Sort", merge_sort), ("Quick Sort", quick_sort)]
    
    for size in data_sizes:
        print(f"\n--- Ukuran Data: {size} ---")
        # Membuat data acak
        data = [random.randint(1, 100000) for _ in range(size)]
        
        for name, func in algorithms:
            # Bubble Sort sangat lambat untuk 50.000 data, 
            # kita beri peringatan agar tidak menunggu terlalu lama
            if name == "Bubble Sort" and size > 10000:
                print(f"{name}: Dilewati (Terlalu lambat untuk data > 10.000)")
                continue
                
            times = []
            for _ in range(3):
                start = time.time()
                func(data)
                end = time.time()
                times.append(end - start)
            
            avg_time = sum(times) / 3
            print(f"{name}: Rata-rata {avg_time:.5f} detik")

if __name__ == "__main__":
    benchmark()