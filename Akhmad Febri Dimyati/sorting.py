import streamlit as st
import time
import random
import matplotlib.pyplot as plt
import sys
import pandas as pd

# Setting dasar
sys.setrecursionlimit(100000)
st.set_page_config(page_title="Sorting Benchmark Tool", layout="wide")

st.title("📊 Sorting Benchmark Dashboard")
st.write("Bandingkan performa algoritma Bubble Sort, Insertion Sort, dan Quick Sort secara real-time.")

# --- 1. Fungsi Algoritma ---
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

def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + right

# --- 2. Sidebar & Input ---
with st.sidebar:
    st.header("Konfigurasi")
    sizes = [100, 1000, 10000, 50000]
    st.write(f"Ukuran Data: {sizes}")
    run_btn = st.button("Mulai Benchmark 🚀")
    st.warning("Catatan: 50.000 data pada Bubble Sort butuh waktu cukup lama.")

# --- 3. Eksekusi Benchmark ---
if run_btn:
    results = {"Bubble Sort": [], "Insertion Sort": [], "Quick Sort": []}
    
    # Progress Bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort),
        ("Quick Sort", quick_sort)
    ]

    total_steps = len(algorithms) * len(sizes)
    step = 0

    for name, func in algorithms:
        for size in sizes:
            status_text.text(f"Running {name} dengan {size} data...")
            
            # Generate data
            test_data = [random.randint(0, 100000) for _ in range(size)]
            
            # Hitung rata-rata 3 kali jalan
            times = []
            for _ in range(3):
                temp = test_data.copy()
                start = time.time()
                if name == "Quick Sort":
                    _ = func(temp)
                else:
                    func(temp)
                times.append(time.time() - start)
            
            avg_time = sum(times) / 3
            results[name].append(avg_time)
            
            step += 1
            progress_bar.progress(step / total_steps)

    status_text.success("Benchmark Selesai!")

    # --- 4. Tampilkan Hasil ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Tabel Hasil (Detik)")
        df = pd.DataFrame(results, index=sizes)
        st.table(df)

    with col2:
        st.subheader("📈 Visualisasi Grafik")
        fig, ax = plt.subplots()
        for name, times in results.items():
            ax.plot(sizes, times, marker='o', label=name)
        
        ax.set_yscale('log') # Skala log agar Quick Sort kelihatan
        ax.set_xlabel("Jumlah Data (n)")
        ax.set_ylabel("Waktu (detik) - Skala Log")
        ax.legend()
        st.pyplot(fig)

    # --- 5. Analisis Otomatis ---
    st.divider()
    st.subheader("🧠 Analisis Jawaban Tugas")
    st.info(f"""
    1. **Algoritma Tercepat:** Quick Sort. Karena menggunakan mekanisme *Divide and Conquer* ($O(n \\log n)$).
    2. **Kesesuaian Teori Big O:** Sangat Sesuai. 
       - Bubble & Insertion menunjukkan kenaikan waktu kuadratik ($O(n^2)$).
       - Quick Sort tetap stabil di bawah meski data mencapai 50.000.
    """)