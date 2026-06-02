import streamlit as st
import time

st.set_page_config(page_title="Visualisasi Searching", layout="wide")

st.title("🔍 Visualisasi Algoritma Searching")

# Konfigurasi Input
with st.sidebar:
    st.header("Konfigurasi")
    n = st.slider("Jumlah Elemen", 10, 50, 20)
    target = st.number_input("Cari Angka:", value=15)
    speed = st.slider("Kecepatan (detik)", 0.1, 1.0, 0.3)
    algo = st.selectbox("Pilih Algoritma", ["Linear Search", "Binary Search"])

# Generate Data
if 'data' not in st.session_state or st.button("Generate Data Baru"):
    import random
    st.session_state.data = sorted([random.randint(1, 100) for _ in range(n)])

data = st.session_state.data
cols = st.columns(len(data))

# Fungsi Visualisasi Bar
def draw_bars(current_idx=-1, found_idx=-1, low=-1, high=-1):
    for i, val in enumerate(data):
        color = "white"
        if i == found_idx: color = "green"
        elif i == current_idx: color = "yellow"
        elif low <= i <= high and algo == "Binary Search": color = "blue"
        
        cols[i].markdown(
            f"<div style='background-color:{color}; height:{val*2}px; border:1px solid black; text-align:center; color:black;'>{val}</div>", 
            unsafe_allow_html=True
        )

# Logika Algoritma
if st.button("Mulai Cari"):
    found = False
    
    if algo == "Linear Search":
        for i in range(len(data)):
            draw_bars(current_idx=i)
            if data[i] == target:
                draw_bars(found_idx=i)
                st.success(f"Ditemukan di indeks {i}")
                found = True
                break
            time.sleep(speed)
            
    else: # Binary Search
        low, high = 0, len(data) - 1
        while low <= high:
            mid = (low + high) // 2
            draw_bars(current_idx=mid, low=low, high=high)
            time.sleep(speed)
            
            if data[mid] == target:
                draw_bars(found_idx=mid)
                st.success(f"Ditemukan di indeks {mid}")
                found = True
                break
            elif data[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
    
    if not found:
        st.error("Data tidak ditemukan")