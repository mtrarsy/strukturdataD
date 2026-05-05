import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Sorting Algorithm Benchmark")

# ==============================
# ALGORITMA SORTING
# ==============================

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


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
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# ==============================
# PILIHAN USER
# ==============================

sizes = st.multiselect(
    "Pilih Ukuran Data",
    [100, 1000, 10000, 50000],
    default=[100, 1000, 10000]
)

runs = st.slider("Jumlah Percobaan", 3, 10, 3)

algorithms = {
    "Bubble Sort": bubble_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}

if st.button("🚀 Jalankan Benchmark"):

    results = {name: [] for name in algorithms}

    for size in sizes:
        for name, func in algorithms.items():
            total_time = 0

            for _ in range(runs):
                data = [random.randint(1, 100000) for _ in range(size)]
                data_copy = data.copy()

                start = time.perf_counter()
                func(data_copy)
                end = time.perf_counter()

                total_time += (end - start)

            avg_time = total_time / runs
            results[name].append(avg_time)

    # ==============================
    # TABEL HASIL
    # ==============================

    df = pd.DataFrame(results, index=sizes)
    df.index.name = "Ukuran Data"

    st.subheader("📋 Tabel Hasil Benchmark (Rata-rata detik)")
    st.dataframe(df)

    # ==============================
    # GRAFIK
    # ==============================

    st.subheader("📈 Grafik Perbandingan")

    plt.figure()

    for name in algorithms:
        plt.plot(sizes, df[name], marker='o', label=name)

    plt.xlabel("Ukuran Data")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)

    # ==============================
    # ANALISIS OTOMATIS
    # ==============================

    st.subheader("🧠 Analisis")

    fastest = df.mean().idxmin()
    slowest = df.mean().idxmax()

    st.write(f"✅ Algoritma tercepat (rata-rata keseluruhan): **{fastest}**")
    st.write(f"❌ Algoritma paling lambat: **{slowest}**")

    st.write("""
    **Penjelasan Teori Big-O:**
    - Bubble Sort → O(n²)
    - Merge Sort → O(n log n)
    - Quick Sort → O(n log n) rata-rata

    Hasil biasanya sesuai teori karena algoritma dengan kompleksitas O(n²)
    akan jauh lebih lambat dibanding O(n log n) saat data besar.
    """)

    st.success("Benchmark selesai!")