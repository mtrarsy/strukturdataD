import streamlit as st
import time

st.set_page_config(page_title="Searching Algorithm Visualizer", page_icon="🔍", layout="wide")

st.title("🔍 Searching Algorithm Visualizer")
st.caption("Struktur Data — Informatika UINSSC | MMXXVI")

# ─── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Konfigurasi")

algorithm = st.sidebar.radio(
    "Pilih Algoritma",
    ["Sequential Search (Linear)", "Binary Search"],
    help="Binary Search memerlukan array terurut"
)

default_arr = "10, 50, 30, 70, 80, 60, 20, 90, 40"
if algorithm == "Binary Search":
    default_arr = "2, 5, 8, 12, 16, 23, 38, 56, 72, 91"

arr_input = st.sidebar.text_input(
    "Array (pisah dengan koma)",
    value=default_arr
)

key_input = st.sidebar.number_input("Key yang dicari", value=30, step=1)
speed = st.sidebar.slider("Kecepatan animasi (detik)", 0.1, 2.0, 0.6, step=0.1)

# ─── Parse input ──────────────────────────────────────────────────────────────
try:
    arr = [int(x.strip()) for x in arr_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("❌ Format array tidak valid. Gunakan angka yang dipisah koma.")
    st.stop()

# ─── Helper: render array ─────────────────────────────────────────────────────
def render_array(arr, highlight=None, found=None, eliminated=None, lo=None, hi=None, mid=None):
    """Render array sebagai tabel berwarna menggunakan HTML."""
    cells = ""
    for i, val in enumerate(arr):
        if found is not None and i == found:
            bg, color, border = "#C0DD97", "#27500A", "2px solid #3B6D11"
            label = "✓ Found"
        elif eliminated and i in eliminated:
            bg, color, border = "#f0f0f0", "#aaa", "1px solid #ccc"
            label = ""
        elif mid is not None and i == mid:
            bg, color, border = "#B5D4F4", "#0C447C", "2px solid #185FA5"
            label = "Mid"
        elif highlight is not None and i == highlight:
            bg, color, border = "#CECBF6", "#3C3489", "2px solid #534AB7"
            label = "Cur"
        elif lo is not None and i == lo:
            bg, color, border = "#EEEDFE", "#3C3489", "1.5px solid #AFA9EC"
            label = "Low"
        elif hi is not None and i == hi:
            bg, color, border = "#FAECE7", "#712B13", "1.5px solid #F0997B"
            label = "High"
        else:
            bg, color, border = "#f8f8f8", "#333", "1px solid #ddd"
            label = ""

        cells += f"""
        <td style="text-align:center; padding:4px 8px;">
            <div style="font-size:11px; color:#999; margin-bottom:2px;">[{i}]</div>
            <div style="
                background:{bg}; color:{color};
                border:{border}; border-radius:8px;
                width:52px; height:52px;
                display:flex; align-items:center; justify-content:center;
                font-size:18px; font-weight:600; margin:auto;
            ">{val}</div>
            <div style="font-size:11px; color:#666; margin-top:3px; min-height:14px;">{label}</div>
        </td>
        """

    html = f"""
    <div style="overflow-x:auto; padding:8px 0;">
        <table style="border-collapse:separate; border-spacing:4px; margin:auto;">
            <tr>{cells}</tr>
        </table>
    </div>
    """
    return html

# ─── Sequential Search ────────────────────────────────────────────────────────
def sequential_search(arr, key):
    steps = []
    for i in range(len(arr)):
        if arr[i] == key:
            steps.append({
                "highlight": i, "found": i,
                "eliminated": list(range(i)),
                "log": f"✅ **Ditemukan!** arr[{i}] = {arr[i]} sama dengan key = {key}",
                "step": i + 1
            })
            return steps, i
        steps.append({
            "highlight": i,
            "eliminated": list(range(i)),
            "found": None,
            "log": f"🔎 Langkah {i+1}: arr[{i}] = {arr[i]} ≠ {key} → lanjut",
            "step": i + 1
        })
    steps.append({
        "highlight": None,
        "eliminated": list(range(len(arr))),
        "found": None,
        "log": f"❌ Key **{key}** tidak ditemukan dalam array.",
        "step": len(arr) + 1
    })
    return steps, -1

# ─── Binary Search ────────────────────────────────────────────────────────────
def binary_search(arr, key):
    sorted_arr = sorted(arr)
    steps = []
    lo, hi = 0, len(sorted_arr) - 1
    step_num = 1

    while lo <= hi:
        mid = (lo + hi) // 2
        elim = list(range(0, lo)) + list(range(hi + 1, len(sorted_arr)))

        if sorted_arr[mid] == key:
            steps.append({
                "arr": sorted_arr, "lo": lo, "hi": hi, "mid": mid,
                "found": mid, "eliminated": elim,
                "log": f"✅ **Ditemukan!** arr[{mid}] = {sorted_arr[mid]} sama dengan key = {key}",
                "step": step_num
            })
            return steps, mid, sorted_arr
        elif sorted_arr[mid] < key:
            steps.append({
                "arr": sorted_arr, "lo": lo, "hi": hi, "mid": mid,
                "found": None, "eliminated": elim,
                "log": f"🔎 Langkah {step_num}: Low={lo}, Mid={mid}, High={hi} → arr[{mid}]={sorted_arr[mid]} < {key} → **Low = {mid+1}**",
                "step": step_num
            })
            lo = mid + 1
        else:
            steps.append({
                "arr": sorted_arr, "lo": lo, "hi": hi, "mid": mid,
                "found": None, "eliminated": elim,
                "log": f"🔎 Langkah {step_num}: Low={lo}, Mid={mid}, High={hi} → arr[{mid}]={sorted_arr[mid]} > {key} → **High = {mid-1}**",
                "step": step_num
            })
            hi = mid - 1
        step_num += 1

    steps.append({
        "arr": sorted_arr, "lo": lo, "hi": hi, "mid": -1,
        "found": None, "eliminated": list(range(len(sorted_arr))),
        "log": f"❌ Key **{key}** tidak ditemukan.",
        "step": step_num
    })
    return steps, -1, sorted_arr

# ─── Main UI ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"Algoritma: {algorithm}")

with col2:
    run_btn = st.button("▶ Jalankan", use_container_width=True, type="primary")

# Placeholders
arr_placeholder = st.empty()
log_placeholder = st.empty()

# Complexity info
if algorithm == "Sequential Search (Linear)":
    c1, c2, c3 = st.columns(3)
    c1.metric("Best Case", "O(1)")
    c2.metric("Average Case", "O(N)")
    c3.metric("Worst Case", "O(N)")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Best Case", "O(1)")
    c2.metric("Average Case", "O(log N)")
    c3.metric("Worst Case", "O(log N)")

# Render initial array
arr_placeholder.markdown(render_array(arr), unsafe_allow_html=True)

# ─── Run animation ────────────────────────────────────────────────────────────
if run_btn:
    key = int(key_input)

    if algorithm == "Sequential Search (Linear)":
        steps, result_idx = sequential_search(arr, key)
        display_arr = arr

        for s in steps:
            html = render_array(
                display_arr,
                highlight=s["highlight"],
                found=s["found"],
                eliminated=s["eliminated"]
            )
            arr_placeholder.markdown(html, unsafe_allow_html=True)
            log_placeholder.info(s["log"])
            time.sleep(speed)

    else:
        steps, result_idx, sorted_arr = binary_search(arr, key)

        st.caption(f"Array setelah diurutkan: {sorted_arr}")

        for s in steps:
            html = render_array(
                s["arr"],
                lo=s.get("lo"),
                hi=s.get("hi"),
                mid=s.get("mid") if s.get("found") is None else None,
                found=s.get("found"),
                eliminated=s.get("eliminated", [])
            )
            arr_placeholder.markdown(html, unsafe_allow_html=True)
            log_placeholder.info(s["log"])
            time.sleep(speed)

    if result_idx >= 0:
        st.success(f"🎉 Key **{key}** ditemukan pada indeks **{result_idx}** setelah **{len(steps)}** langkah!")
    else:
        st.error(f"😔 Key **{key}** tidak ditemukan dalam array setelah **{len(steps)-1}** langkah.")

# ─── Penjelasan algoritma ─────────────────────────────────────────────────────
with st.expander("📖 Penjelasan Algoritma"):
    if algorithm == "Sequential Search (Linear)":
        st.markdown("""
### Sequential Search (Linear Search)
- Pencarian data dilakukan **secara urut** dari elemen pertama sampai elemen terakhir.
- Cocok untuk array **tidak terurut** maupun terurut.
- Bekerja pada **array** maupun **linked-list**.

**Algoritma:**
1. Input key (data yang dicari)
2. Bandingkan key dengan setiap elemen dari indeks 0 sampai n-1
3. Jika ditemukan → kembalikan indeksnya
4. Jika tidak ditemukan → kembalikan -1
        """)
    else:
        st.markdown("""
### Binary Search
- Pencarian dimulai dari **pertengahan** array yang sudah **terurut**.
- Setiap iterasi membuang **separuh** data yang tidak relevan.
- **Hanya bisa digunakan** pada sorted array.

**Algoritma:**
1. Tentukan Low = 0, High = N-1
2. Hitung Mid = (Low + High) / 2
3. Jika arr[Mid] == key → selesai
4. Jika key > arr[Mid] → Low = Mid + 1
5. Jika key < arr[Mid] → High = Mid - 1
6. Ulangi hingga ditemukan atau Low > High
        """)