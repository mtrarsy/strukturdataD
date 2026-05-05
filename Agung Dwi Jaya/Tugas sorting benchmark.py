import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

# --- PENGATURAN HALAMAN STREAMLIT ---
st.set_page_config(page_title="Benchmark Sorting", layout="centered")

# --- 1. FUNGSI ALGORITMA SORTING ---
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# --- 2. FUNGSI BENCHMARK ---
@st.cache_data # Mencegah perhitungan ulang saat halaman di-refresh
def run_benchmark():
    sizes = [100, 1000, 10000, 50000]
    results = []

    for size in sizes:
        # Generate data acak
        data = [random.randint(0, 100000) for _ in range(size)]
        row = {"Ukuran Data": size}

        # Menguji Bubble Sort (Lewati jika data >= 50000)
        if size >= 50000:
            row["Bubble Sort"] = None
        else:
            arr_copy = data.copy()
            start = time.time()
            bubble_sort(arr_copy)
            row["Bubble Sort"] = time.time() - start

        # Menguji Insertion Sort (Lewati jika data >= 50000)
        if size >= 50000:
            row["Insertion Sort"] = None
        else:
            arr_copy = data.copy()
            start = time.time()
            insertion_sort(arr_copy)
            row["Insertion Sort"] = time.time() - start

        # Menguji Merge Sort
        arr_copy = data.copy()
        start = time.time()
        merge_sort(arr_copy)
        row["Merge Sort"] = time.time() - start

        results.append(row)

    return pd.DataFrame(results)

# --- 3. TAMPILAN WEB STREAMLIT ---

# Jalankan benchmark dengan indikator loading
with st.spinner("Sedang menghitung benchmark... Mohon tunggu!"):
    df = run_benchmark()

# --- BAGIAN TABEL ---
st.markdown("### 📋 Tabel Hasil Benchmarking (Detik)")

# Mewarnai background kolom Merge Sort menjadi hijau terang
styled_df = df.style.set_properties(**{'background-color': '#90ee90', 'color': 'black'}, subset=['Merge Sort']) \
                    .format("{:.6f}", subset=["Bubble Sort", "Insertion Sort", "Merge Sort"], na_rep="None")

# Menampilkan tabel
st.dataframe(styled_df, use_container_width=True)


# --- BAGIAN GRAFIK ---
st.markdown("### 📈 Visualisasi Grafik")

# Menggunakan Matplotlib untuk membuat grafik garis
fig, ax = plt.subplots(figsize=(8, 5))

# Plot data masing-masing algoritma
ax.plot(df["Ukuran Data"], df["Bubble Sort"], marker='o', label='Bubble Sort', color='#1f77b4')
ax.plot(df["Ukuran Data"], df["Insertion Sort"], marker='o', label='Insertion Sort', color='#ff7f0e')
ax.plot(df["Ukuran Data"], df["Merge Sort"], marker='o', label='Merge Sort', color='#2ca02c')

# Konfigurasi tampilan grafik
ax.set_title("Perbandingan Kecepatan Algoritma Sorting")
ax.set_xlabel("Ukuran Data (n)")
ax.set_ylabel("Waktu (Detik)")
ax.legend()
ax.grid(True, linestyle='-', alpha=0.7)

# Menampilkan grafik ke Streamlit
st.pyplot(fig)