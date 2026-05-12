import streamlit as st
import time

# --- FUNGSI SEARCHING ---
def linear_search_visual(arr, target):
    for i in range(len(arr)):
        yield i, False  # Mengirimkan index yang sedang diperiksa
        if arr[i] == target:
            yield i, True
            return
    yield -1, False

def binary_search_visual(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        yield low, high, mid, False
        if arr[mid] == target:
            yield low, high, mid, True
            return
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    yield low, high, -1, False

# --- FUNGSI HASHING ---
class SimpleHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size

    def _hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash_function(key)
        if self.table[index] is None:
            self.table[index] = []
        # Update jika key sudah ada (Chaining)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def get(self, key):
        index = self._hash_function(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return "Tidak ditemukan"

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Tugas Struktur Data", layout="wide")
st.title("Visualisasi Searching & Implementasi Hashing")
st.write("Informatika UINSSC MMXXVI")

tabs = st.tabs(["🔍 Visualisasi Searching", "🔑 Implementasi Hashing"])

# TAB 1: SEARCHING
with tabs[0]:
    st.header("Algoritma Searching")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        method = st.selectbox("Pilih Metode", ["Linear Search", "Binary Search"])
        target = st.number_input("Cari Angka", value=42)
        speed = st.slider("Kecepatan (detik)", 0.1, 1.0, 0.3)
        
        # Data dummy
        data = [10, 23, 35, 42, 50, 67, 71, 88, 90, 99]
        if method == "Linear Search":
            # Acak urutan untuk linear search agar lebih variatif
            data = [23, 99, 42, 10, 88, 35, 71, 67, 50, 90]
            
        st.write("**Data:**", data)

    with col2:
        if st.button(f"Mulai {method}"):
            placeholders = st.columns(len(data))
            
            if method == "Linear Search":
                found = False
                for idx, is_found in linear_search_visual(data, target):
                    for i in range(len(data)):
                        color = "green" if (i == idx and is_found) else ("yellow" if i == idx else "gray")
                        placeholders[i].markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px; text-align:center; color:white;'>{data[i]}</div>", unsafe_allow_html=True)
                    
                    if is_found:
                        st.success(f"Ditemukan di indeks {idx}")
                        found = True
                        break
                    time.sleep(speed)
                if not found: st.error("Data tidak ditemukan")

            else:  # Binary Search
                found = False
                for low, high, mid, is_found in binary_search_visual(data, target):
                    for i in range(len(data)):
                        if i == mid and is_found: color = "green"
                        elif i == mid: color = "yellow"
                        elif low <= i <= high: color = "blue"
                        else: color = "gray"
                        placeholders[i].markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px; text-align:center; color:white;'>{data[i]}</div>", unsafe_allow_html=True)
                    
                    if is_found:
                        st.success(f"Ditemukan di indeks {mid}")
                        found = True
                        break
                    if mid == -1: break
                    time.sleep(speed)
                if not found: st.error("Data tidak ditemukan")

# TAB 2: HASHING
with tabs[1]:
    st.header("Hash Table (Separate Chaining)")
    
    if 'hash_table' not in st.session_state:
        st.session_state.hash_table = SimpleHashTable(size=5)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Input Data")
        key_input = st.text_input("Key (Nama/ID)")
        val_input = st.text_input("Value (Data)")
        if st.button("Simpan ke Hash Table"):
            if key_input:
                st.session_state.hash_table.insert(key_input, val_input)
                st.toast("Data disimpan!")
    
    with c2:
        st.subheader("Cari Data")
        search_key = st.text_input("Cari berdasarkan Key")
        if st.button("Cari"):
            result = st.session_state.hash_table.get(search_key)
            st.info(f"Hasil: {result}")

    st.divider()
    st.subheader("Struktur Hash Table")
    for i, bucket in enumerate(st.session_state.hash_table.table):
        st.text(f"Index {i}: {bucket}")