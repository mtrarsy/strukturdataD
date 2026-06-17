import streamlit as st
import time
 
st.set_page_config(page_title="Searching Algorithm Visualizer", layout="wide")
 
st.title("🔍 Searching Algorithm Visualizer")
st.caption("Struktur Data — Informatika UINSSC MMXXVI")
 
algorithm = st.sidebar.selectbox(
    "Pilih Algoritma",
    ["Sequential Search (Linear Search)", "Binary Search"]
)
 
st.sidebar.markdown("---")
st.sidebar.markdown("**Masukkan Data Array**")
 
default_data = "10, 50, 30, 70, 80, 60, 20, 90, 40"
raw_input = st.sidebar.text_input("Data (pisahkan dengan koma):", value=default_data)
 
try:
    data = [int(x.strip()) for x in raw_input.split(",") if x.strip()]
except ValueError:
    st.error("Input tidak valid. Masukkan angka yang dipisahkan koma.")
    st.stop()
 
key = st.sidebar.number_input("Kunci (Key) yang dicari:", value=30, step=1)
speed = st.sidebar.slider("Kecepatan animasi (detik)", 0.1, 2.0, 0.5, 0.1)
 
st.sidebar.markdown("---")
start_btn = st.sidebar.button("▶ Mulai Pencarian", type="primary", use_container_width=True)
reset_btn = st.sidebar.button("↺ Reset", use_container_width=True)
 
 
def render_array(arr, current=-1, found=-1, low=-1, high=-1, mid=-1, label=""):
    cols = st.columns(len(arr))
    for i, val in enumerate(arr):
        with cols[i]:
            if i == found:
                st.markdown(
                    f"<div style='text-align:center; background:#d4edda; border:2px solid #28a745;"
                    f"border-radius:8px; padding:8px 0; font-weight:bold; color:#155724'>"
                    f"<small style='color:#155724'>idx {i}</small><br>{val}</div>",
                    unsafe_allow_html=True
                )
            elif i == current and found == -1:
                st.markdown(
                    f"<div style='text-align:center; background:#fff3cd; border:2px solid #ffc107;"
                    f"border-radius:8px; padding:8px 0; font-weight:bold; color:#856404'>"
                    f"<small style='color:#856404'>idx {i}</small><br>{val}</div>",
                    unsafe_allow_html=True
                )
            elif i == mid and found == -1:
                st.markdown(
                    f"<div style='text-align:center; background:#cce5ff; border:2px solid #004085;"
                    f"border-radius:8px; padding:8px 0; font-weight:bold; color:#004085'>"
                    f"<small style='color:#004085'>MID</small><br>{val}</div>",
                    unsafe_allow_html=True
                )
            elif low <= i <= high and high != -1:
                st.markdown(
                    f"<div style='text-align:center; background:#e2d9f3; border:1px solid #6f42c1;"
                    f"border-radius:8px; padding:8px 0; color:#4a1e8c'>"
                    f"<small style='color:#4a1e8c'>idx {i}</small><br>{val}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='text-align:center; background:#f8f9fa; border:1px solid #dee2e6;"
                    f"border-radius:8px; padding:8px 0; color:#495057'>"
                    f"<small style='color:#6c757d'>idx {i}</small><br>{val}</div>",
                    unsafe_allow_html=True
                )
    if label:
        st.caption(label)
 
 
def sequential_search(arr, key, speed):
    steps = 0
    comparisons = 0
    log = []
 
    for i in range(len(arr)):
        steps += 1
        comparisons += 1
        status_placeholder.info(f"🔎 Membandingkan: arr[{i}] = **{arr[i]}** dengan Key = **{key}**")
        array_placeholder.empty()
        with array_placeholder.container():
            render_array(arr, current=i, label=f"Step {steps}: Periksa index {i} → nilai {arr[i]}")
 
        if arr[i] == key:
            log.append(f"✅ Ditemukan! arr[{i}] = {key}")
            with array_placeholder.container():
                render_array(arr, found=i, label=f"✅ Key {key} ditemukan di index {i}!")
            status_placeholder.success(f"✅ Key **{key}** ditemukan di index **{i}**!")
            return i, steps, comparisons, log
        else:
            log.append(f"❌ arr[{i}] = {arr[i]} ≠ {key}")
            time.sleep(speed)
 
    status_placeholder.error(f"❌ Key **{key}** tidak ditemukan dalam array.")
    log.append(f"❌ Key {key} tidak ditemukan.")
    return -1, steps, comparisons, log
 
 
def binary_search(arr, key, speed):
    sorted_arr = sorted(arr)
    st.info(f"⚙️ Array diurutkan terlebih dahulu: {sorted_arr}")
    time.sleep(speed)
 
    low = 0
    high = len(sorted_arr) - 1
    steps = 0
    comparisons = 0
    log = []
 
    while low <= high:
        mid = (low + high) // 2
        steps += 1
        comparisons += 1
 
        status_placeholder.info(
            f"🔎 Step {steps}: Low={low}, Mid={mid}, High={high} | arr[Mid]={sorted_arr[mid]} vs Key={key}"
        )
        with array_placeholder.container():
            render_array(sorted_arr, low=low, high=high, mid=mid,
                         label=f"Low={low} | Mid={mid} | High={high}")
 
        time.sleep(speed)
 
        if sorted_arr[mid] == key:
            log.append(f"✅ Ditemukan! arr[{mid}] = {key}")
            with array_placeholder.container():
                render_array(sorted_arr, found=mid, label=f"✅ Key {key} ditemukan di index {mid}!")
            status_placeholder.success(f"✅ Key **{key}** ditemukan di index **{mid}** (array terurut)!")
            return mid, steps, comparisons, log
        elif sorted_arr[mid] < key:
            log.append(f"arr[{mid}]={sorted_arr[mid]} < {key} → cari di kanan (low={mid+1})")
            low = mid + 1
        else:
            log.append(f"arr[{mid}]={sorted_arr[mid]} > {key} → cari di kiri (high={mid-1})")
            high = mid - 1
 
    status_placeholder.error(f"❌ Key **{key}** tidak ditemukan.")
    log.append(f"❌ Key {key} tidak ditemukan.")
    return -1, steps, comparisons, log
 
 
col1, col2 = st.columns([3, 1])
 
with col1:
    st.markdown(f"**Array saat ini:** `{data}`")
    st.markdown(f"**Key yang dicari:** `{key}`")
 
with col2:
    n = len(data)
    if algorithm == "Sequential Search (Linear Search)":
        st.markdown("**Kompleksitas:**")
        st.markdown("- Best: O(1)\n- Avg: O(N)\n- Worst: O(N)")
    else:
        st.markdown("**Kompleksitas:**")
        st.markdown("- Best: O(1)\n- Avg: O(log N)\n- Worst: O(log N)")
 
st.markdown("---")
 
legend_cols = st.columns(4)
with legend_cols[0]:
    st.markdown(
        "<span style='background:#fff3cd;border:2px solid #ffc107;padding:2px 10px;"
        "border-radius:5px;font-size:13px;color:#856404'>⬛ Sedang diperiksa</span>",
        unsafe_allow_html=True
    )
with legend_cols[1]:
    st.markdown(
        "<span style='background:#d4edda;border:2px solid #28a745;padding:2px 10px;"
        "border-radius:5px;font-size:13px;color:#155724'>✅ Ditemukan</span>",
        unsafe_allow_html=True
    )
with legend_cols[2]:
    st.markdown(
        "<span style='background:#cce5ff;border:2px solid #004085;padding:2px 10px;"
        "border-radius:5px;font-size:13px;color:#004085'>🔵 Posisi Mid</span>",
        unsafe_allow_html=True
    )
with legend_cols[3]:
    st.markdown(
        "<span style='background:#e2d9f3;border:1px solid #6f42c1;padding:2px 10px;"
        "border-radius:5px;font-size:13px;color:#4a1e8c'>🟣 Rentang aktif</span>",
        unsafe_allow_html=True
    )
 
st.markdown("---")
 
array_placeholder = st.empty()
status_placeholder = st.empty()
 
with array_placeholder.container():
    render_array(data, label="Array awal (belum ada pencarian)")
 
if start_btn:
    status_placeholder.info("🚀 Memulai pencarian...")
    time.sleep(0.3)
 
    if algorithm == "Sequential Search (Linear Search)":
        result_idx, steps, comparisons, log = sequential_search(data, key, speed)
    else:
        result_idx, steps, comparisons, log = binary_search(data, key, speed)
 
    st.markdown("---")
    st.subheader("📊 Hasil & Statistik")
    c1, c2, c3 = st.columns(3)
    c1.metric("Jumlah Langkah", steps)
    c2.metric("Perbandingan", comparisons)
    c3.metric("Status", "Ditemukan ✅" if result_idx != -1 else "Tidak Ditemukan ❌")
 
    with st.expander("📋 Log Langkah-langkah"):
        for entry in log:
            st.markdown(f"- {entry}")
 
if reset_btn:
    st.rerun()
 