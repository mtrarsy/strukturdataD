import streamlit as st
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

# --- ALGORITMA SORTING ---

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
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
    return arr

# --- FUNGSI BENCHMARK ---

def benchmark(sizes, iterations=3):
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort
    }
    
    results = []
    
    for size in sizes:
        st.write(f"⏳ Menjalankan benchmark untuk ukuran data: **{size}**...")
        row = {"Ukuran Data": size}
        
        for name, func in algorithms.items():
            # Batasi bubble/insertion sort pada data besar agar tidak hang (opsional)
            if size > 10000 and name in ["Bubble Sort", "Insertion Sort"]:
                row[name] = None
                continue
                
            times = []
            for _ in range(iterations):
                data = [random.randint(0, 100000) for _ in range(size)]
                start_time = time.time()
                func(data)
                end_time = time.time()
                times.append(end_time - start_time)
            
            avg_time = sum(times) / iterations
            row[name] = avg_time
            
        results.append(row)
    
    return pd.DataFrame(results)

# --- UI STREAMLIT ---

st.set_page_config(page_title="Sorting Benchmark", layout="wide")
st.title("📊 Sorting Algorithm Benchmarking")
st.write("Aplikasi ini membandingkan kecepatan Bubble Sort, Insertion Sort, dan Merge Sort.")

# Sidebar Input
st.sidebar.header("Konfigurasi")
input_sizes = st.sidebar.multiselect(
    "Pilih Ukuran Data:", 
    [100, 1000, 10000, 50000], 
    default=[100, 1000, 10000]
)
run_button = st.sidebar.button("Mulai Benchmark")

if run_button:
    # Eksekusi Benchmark
    df_results = benchmark(input_sizes)
    
    # 1. Tabel Hasil
    st.subheader("📋 Tabel Hasil Benchmarking (Detik)")
    st.dataframe(df_results.style.highlight_min(axis=1, color='lightgreen'))

    # 2. Visualisasi Grafik
    st.subheader("📈 Visualisasi Grafik")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for col in df_results.columns[1:]:
        ax.plot(df_results["Ukuran Data"], df_results[col], marker='o', label=col)
    
    ax.set_xlabel("Ukuran Data (n)")
    ax.set_ylabel("Waktu (Detik)")
    ax.set_title("Perbandingan Kecepatan Algoritma Sorting")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)



else:
    st.info("Klik tombol 'Mulai Benchmark' di sidebar untuk melihat perbandingan.")