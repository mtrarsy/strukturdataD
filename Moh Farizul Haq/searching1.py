import streamlit as st
import time

st.set_page_config(page_title="Visualisasi Searching", layout="centered")

st.title("🔍 Visualisasi Algoritma Searching")
st.write("Aplikasi ini memvisualisasikan cara kerja **Linear Search** dan **Binary Search**.")

# Input Data dari Pengguna
data_input = st.text_input("Masukkan kumpulan angka (pisahkan dengan koma):", "12, 45, 7, 23, 56, 34, 90")
target_input = st.number_input("Masukkan angka yang ingin dicari:", value=23)
algo = st.selectbox("Pilih Algoritma Searching:", ["Linear Search", "Binary Search"])

# Konversi input teks ke list integer
try:
    array = [int(x.strip()) for x in data_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("Format salah! Pastikan hanya memasukkan angka yang dipisahkan koma.")
    array = []

if st.button("Mulai Pencarian"):
    if not array:
        st.warning("Silakan masukkan data angka terlebih dahulu.")
    else:
        # --- LINEAR SEARCH ---
        if algo == "Linear Search":
            st.subheader("Proses Linear Search (Cek satu per satu):")
            found = False
            placeholder = st.empty()
            
            for i in range(len(array)):
                # Visualisasi proses pengecekan indeks
                with placeholder.container():
                    cols = st.columns(len(array))
                    for idx, col in enumerate(cols):
                        if idx == i:
                            col.metric(label=f"Indeks {idx}", value=array[idx], delta="Dicek", delta_color="off")
                        else:
                            col.metric(label=f"Indeks {idx}", value=array[idx])
                
                time.sleep(1) # Efek animasi delay 1 detik
                
                if array[i] == target_input:
                    found = True
                    st.success(f"🎯 Ditemukan! Angka {target_input} ada di indeks ke-{i}.")
                    break
            
            if not found:
                st.error(f"❌ Angka {target_input} tidak ditemukan dalam data.")

        # --- BINARY SEARCH ---
        elif algo == "Binary Search":
            st.subheader("Proses Binary Search (Data wajib diurutkan terlebih dahulu):")
            array.sort() # Binary search mengharuskan data terurut
            st.info(f"Data setelah diurutkan otomatis: {array}")
            
            low = 0
            high = len(array) - 1
            found = False
            placeholder = st.empty()
            step = 1
            
            while low <= high:
                mid = (low + high) // 2
                
                with placeholder.container():
                    st.write(f"**Langkah {step}:** Low Indeks={low}, High Indeks={high}, Mid Indeks={mid} (Nilai: {array[mid]})")
                    cols = st.columns(len(array))
                    for idx, col in enumerate(cols):
                        if idx == mid:
                            col.metric(label=f"Mid ({idx})", value=array[idx], delta="Tengah", delta_color="inverse")
                        elif idx == low:
                            col.metric(label=f"Low ({idx})", value=array[idx])
                        elif idx == high:
                            col.metric(label=f"High ({idx})", value=array[idx])
                        else:
                            col.metric(label=f"Indeks {idx}", value=array[idx])
                
                time.sleep(1.5)
                
                if array[mid] == target_input:
                    st.success(f"🎯 Ditemukan! Angka {target_input} ada di indeks ke-{mid}.")
                    found = True
                    break
                elif array[mid] < target_input:
                    low = mid + 1
                else:
                    high = mid - 1
                step += 1
                
            if not found:
                st.error(f"❌ Angka {target_input} tidak ditemukan dalam data.")