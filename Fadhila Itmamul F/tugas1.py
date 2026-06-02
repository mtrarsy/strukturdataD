import streamlit as st
import time
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Tugas Struktur Data", layout="wide")

st.title("🖥️ Tugas Struktur Data: Searching & Hashing")

tab1, tab2 = st.tabs(["Visualisasi Searching", "Implementasi Hashing"])

# --- TAB 1: SEARCHING ---
with tab1:
    st.header("🔍 Visualisasi Algoritma Searching")
    
    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        n = st.slider("Jumlah Elemen", 5, 30, 15)
    with col_input2:
        target = st.number_input("Cari Angka:", value=10)
    with col_input3:
        algo = st.selectbox("Pilih Algoritma", ["Linear Search", "Binary Search"])

    if 'data' not in st.session_state or st.button("Acak Data Baru"):
        st.session_state.data = sorted([random.randint(1, 100) for _ in range(n)])

    data = st.session_state.data
    placeholder = st.empty()

    def draw_bars(current_idx=-1, found_idx=-1, low=-1, high=-1):
        with placeholder.container():
            cols = st.columns(len(data))
            for i, val in enumerate(data):
                color = "#EEEEEE"  # Abu-abu (default)
                if i == found_idx: color = "#28a745"  # Hijau (ketemu)
                elif i == current_idx: color = "#ffc107"  # Kuning (sedang dicek)
                elif low <= i <= high and algo == "Binary Search": color = "#007bff"  # Biru (rentang cari)
                
                cols[i].markdown(
                    f"<div style='background-color:{color}; height:{val*3}px; border-radius:5px; border:1px solid #333; text-align:center; color:black; font-weight:bold;'>{val}</div>", 
                    unsafe_allow_html=True
                )

    if st.button("Mulai Pencarian"):
        found = False
        if algo == "Linear Search":
            for i in range(len(data)):
                draw_bars(current_idx=i)
                time.sleep(0.3)
                if data[i] == target:
                    draw_bars(found_idx=i)
                    st.success(f"Ketemu! Angka {target} ada di indeks {i}")
                    found = True
                    break
        else:
            low, high = 0, len(data) - 1
            while low <= high:
                mid = (low + high) // 2
                draw_bars(current_idx=mid, low=low, high=high)
                time.sleep(0.5)
                if data[mid] == target:
                    draw_bars(found_idx=mid)
                    st.success(f"Ketemu! Angka {target} ada di indeks {mid}")
                    found = True
                    break
                elif data[mid] < target: low = mid + 1
                else: high = mid - 1
        
        if not found:
            draw_bars()
            st.error(f"Angka {target} tidak ditemukan dalam data.")

# --- TAB 2: HASHING ---
with tab2:
    st.header("🗄️ Implementasi Hash Table (Chaining)")

    class HashTable:
        def __init__(self, size):
            self.size = size
            self.table = [[] for _ in range(self.size)]

        def _hash_function(self, key):
            return hash(str(key)) % self.size

        def insert(self, key, value):
            index = self._hash_function(key)
            for pair in self.table[index]:
                if pair == key:
                    pair = value
                    return
            self.table[index].append([key, value])

    # Contoh data
    h = HashTable(size=7)
    h.insert("Nama", "Fadil")
    h.insert("Mata Kuliah", "Struktur Data")
    h.insert("NIM", "12345678")

    st.write("Isi Hash Table saat ini:")
    for i, bucket in enumerate(h.table):
        st.code(f"Bucket {i}: {bucket}")

    st.info("Setiap bucket menggunakan list (Chaining) untuk menangani kolisi.")