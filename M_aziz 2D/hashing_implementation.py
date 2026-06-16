import streamlit as st
import hashlib
from collections import defaultdict
 
st.set_page_config(page_title="Implementasi Hashing", layout="wide")
 
st.title("🗂️ Implementasi Hashing")
st.caption("Struktur Data — Informatika UINSSC MMXXVI")
 
menu = st.sidebar.radio(
    "Pilih Topik",
    ["Hash Table (Modulo)", "Collision: Chaining", "Collision: Linear Probing", "Fungsi Hash Kriptografi"]
)
 
 
def render_hash_table(table, size, highlights=None):
    if highlights is None:
        highlights = {}
    st.markdown("**Tabel Hash:**")
    cols = st.columns([1, 2, 3])
    cols[0].markdown("**Index**")
    cols[1].markdown("**Value**")
    cols[2].markdown("**Keterangan**")
    for i in range(size):
        val = table.get(i, "")
        note = highlights.get(i, "")
        bg = "#d4edda" if note == "baru" else "#fff3cd" if note == "collision" else "#f8f9fa"
        border = "#28a745" if note == "baru" else "#ffc107" if note == "collision" else "#dee2e6"
        cols[0].markdown(
            f"<div style='background:{bg};border:1px solid {border};"
            f"border-radius:6px;padding:6px;text-align:center;font-weight:bold'>{i}</div>",
            unsafe_allow_html=True
        )
        cols[1].markdown(
            f"<div style='background:{bg};border:1px solid {border};"
            f"border-radius:6px;padding:6px;text-align:center'>{val}</div>",
            unsafe_allow_html=True
        )
        if note == "baru":
            cols[2].markdown(f"<span style='color:#28a745;font-size:13px'>✅ Baru dimasukkan</span>", unsafe_allow_html=True)
        elif note == "collision":
            cols[2].markdown(f"<span style='color:#dc3545;font-size:13px'>⚠️ Collision!</span>", unsafe_allow_html=True)
        else:
            cols[2].markdown("—")
 
 
def render_chain_table(chain_table, size):
    st.markdown("**Tabel Hash dengan Chaining:**")
    for i in range(size):
        chain = chain_table.get(i, [])
        if chain:
            nodes = " → ".join(
                [f"<span style='background:#cce5ff;border:1px solid #004085;border-radius:20px;"
                 f"padding:4px 12px;font-weight:bold;color:#004085'>{v}</span>" for v in chain]
            )
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:8px;margin:4px 0'>"
                f"<span style='background:#e2d9f3;border:1px solid #6f42c1;border-radius:6px;"
                f"padding:4px 10px;min-width:40px;text-align:center;font-weight:bold;color:#4a1e8c'>{i}</span>"
                f"<span style='color:#6c757d'>→</span> {nodes}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:8px;margin:4px 0'>"
                f"<span style='background:#f8f9fa;border:1px solid #dee2e6;border-radius:6px;"
                f"padding:4px 10px;min-width:40px;text-align:center;color:#6c757d'>{i}</span>"
                f"<span style='color:#dee2e6'>→ kosong</span></div>",
                unsafe_allow_html=True
            )
 
 
if menu == "Hash Table (Modulo)":
    st.subheader("Hash Table — Fungsi Hash: h(k) = k mod N")
    st.markdown(
        "Fungsi hash sederhana menggunakan **modulo**. Kunci (key) dibagi dengan ukuran tabel "
        "dan sisa baginya menjadi indeks penyimpanan."
    )
 
    col_l, col_r = st.columns([1, 2])
    with col_l:
        table_size = st.number_input("Ukuran Tabel (N):", min_value=2, max_value=20, value=7)
        raw = st.text_input("Masukkan data (angka, pisahkan koma):", value="14, 5, 9, 1, 24")
        insert_btn = st.button("Masukkan ke Tabel Hash", type="primary")
 
    with col_r:
        if insert_btn:
            try:
                items = [int(x.strip()) for x in raw.split(",") if x.strip()]
            except ValueError:
                st.error("Input tidak valid.")
                st.stop()
 
            table = {}
            steps = []
            for item in items:
                idx = item % table_size
                steps.append((item, idx, idx in table))
                if idx not in table:
                    table[idx] = item
 
            st.markdown("**Proses Hashing:**")
            for item, idx, collision in steps:
                color = "#dc3545" if collision else "#28a745"
                icon = "⚠️ Collision" if collision else "✅ Disimpan"
                st.markdown(
                    f"<div style='background:#f8f9fa;border-left:4px solid {color};"
                    f"border-radius:4px;padding:8px 12px;margin:4px 0;font-size:14px'>"
                    f"h({item}) = {item} mod {table_size} = <b>{idx}</b> → {icon}</div>",
                    unsafe_allow_html=True
                )
 
            st.markdown("---")
            highlights = {idx: "baru" for _, idx, col in steps if not col}
            highlights.update({idx: "collision" for _, idx, col in steps if col})
            render_hash_table(table, table_size, highlights)
 
            collisions = sum(1 for _, _, c in steps if c)
            if collisions:
                st.warning(f"⚠️ Terjadi {collisions} collision! Gunakan metode Chaining atau Open Addressing untuk mengatasinya.")
 
 
elif menu == "Collision: Chaining":
    st.subheader("Penanganan Collision — Chaining (Linked List)")
    st.markdown(
        "Ketika terjadi collision, data baru ditambahkan ke **linked list** pada indeks yang sama. "
        "Satu indeks bisa menampung banyak nilai."
    )
 
    col_l, col_r = st.columns([1, 2])
    with col_l:
        table_size = st.number_input("Ukuran Tabel (N):", min_value=2, max_value=20, value=7)
        raw = st.text_input("Masukkan data (angka, pisahkan koma):", value="21, 77, 72, 75, 5, 19")
        insert_btn = st.button("Masukkan dengan Chaining", type="primary")
 
    with col_r:
        if insert_btn:
            try:
                items = [int(x.strip()) for x in raw.split(",") if x.strip()]
            except ValueError:
                st.error("Input tidak valid.")
                st.stop()
 
            chain_table = defaultdict(list)
            st.markdown("**Proses Chaining:**")
            for item in items:
                idx = item % table_size
                collision = len(chain_table[idx]) > 0
                chain_table[idx].append(item)
                icon = "⛓️ Chained" if collision else "✅ Disimpan"
                color = "#ffc107" if collision else "#28a745"
                st.markdown(
                    f"<div style='background:#f8f9fa;border-left:4px solid {color};"
                    f"border-radius:4px;padding:8px 12px;margin:4px 0;font-size:14px'>"
                    f"h({item}) = {item} mod {table_size} = <b>{idx}</b> → {icon}</div>",
                    unsafe_allow_html=True
                )
 
            st.markdown("---")
            render_chain_table(dict(chain_table), table_size)
 
 
elif menu == "Collision: Linear Probing":
    st.subheader("Penanganan Collision — Linear Probing (Open Addressing)")
    st.markdown(
        "Ketika terjadi collision, cari **sel kosong berikutnya** secara berurutan. "
        "Ukuran tabel harus lebih besar dari jumlah data."
    )
 
    col_l, col_r = st.columns([1, 2])
    with col_l:
        table_size = st.number_input("Ukuran Tabel (N):", min_value=3, max_value=20, value=10)
        raw = st.text_input("Masukkan data (angka, pisahkan koma):", value="2001, 13, 11456, 157, 207")
        insert_btn = st.button("Masukkan dengan Linear Probing", type="primary")
 
    with col_r:
        if insert_btn:
            try:
                items = [int(x.strip()) for x in raw.split(",") if x.strip()]
            except ValueError:
                st.error("Input tidak valid.")
                st.stop()
 
            if len(items) >= table_size:
                st.error("Jumlah data harus lebih kecil dari ukuran tabel!")
                st.stop()
 
            table = {}
            highlights = {}
            log = []
            for item in items:
                orig_idx = item % table_size
                idx = orig_idx
                probes = 0
                while idx in table:
                    probes += 1
                    idx = (idx + 1) % table_size
                    if idx == orig_idx:
                        log.append(f"❌ Tabel penuh! Tidak bisa menyimpan {item}.")
                        break
                if idx not in table:
                    table[idx] = item
                    if probes > 0:
                        highlights[idx] = "baru"
                        log.append(
                            f"h({item})={orig_idx} → Collision × {probes}, disimpan di idx {idx} (probing {probes}×)"
                        )
                    else:
                        highlights[idx] = "baru"
                        log.append(f"h({item})={orig_idx} → Disimpan langsung di idx {idx}")
 
            st.markdown("**Log Linear Probing:**")
            for entry in log:
                color = "#dc3545" if "Collision" in entry else "#28a745"
                st.markdown(
                    f"<div style='background:#f8f9fa;border-left:4px solid {color};"
                    f"border-radius:4px;padding:8px 12px;margin:4px 0;font-size:13px'>{entry}</div>",
                    unsafe_allow_html=True
                )
 
            st.markdown("---")
            render_hash_table(table, table_size, highlights)
 
 
elif menu == "Fungsi Hash Kriptografi":
    st.subheader("Fungsi Hash Kriptografi: MD5, SHA-1, SHA-256")
    st.markdown(
        "Fungsi hash kriptografi mengubah input apapun menjadi nilai hash dengan panjang tetap. "
        "Digunakan untuk keamanan data, verifikasi integritas, dan penyimpanan password."
    )
 
    input_text = st.text_input("Masukkan teks untuk di-hash:", value="Struktur Data UINSSC")
    compare_text = st.text_input("Teks pembanding (opsional):", value="Struktur Data UINSSC!")
 
    if input_text:
        st.markdown("---")
        st.markdown("**Hasil Hash:**")
 
        col1, col2 = st.columns(2)
 
        algorithms = [
            ("MD5", hashlib.md5, "128-bit", "#dc3545", "Cepat, tidak aman untuk kriptografi"),
            ("SHA-1", hashlib.sha1, "160-bit", "#ffc107", "Lebih aman dari MD5, sudah usang"),
            ("SHA-256", hashlib.sha256, "256-bit", "#28a745", "Aman, standar industri saat ini"),
        ]
 
        with col1:
            st.markdown(f"**Input 1:** `{input_text}`")
            for name, func, bits, color, note in algorithms:
                h = func(input_text.encode()).hexdigest()
                st.markdown(
                    f"<div style='background:#f8f9fa;border-left:4px solid {color};"
                    f"border-radius:4px;padding:10px 14px;margin:6px 0'>"
                    f"<b style='color:{color}'>{name}</b> ({bits})<br>"
                    f"<code style='font-size:12px;word-break:break-all'>{h}</code><br>"
                    f"<small style='color:#6c757d'>{note}</small></div>",
                    unsafe_allow_html=True
                )
 
        with col2:
            if compare_text:
                st.markdown(f"**Input 2:** `{compare_text}`")
                for name, func, bits, color, note in algorithms:
                    h1 = func(input_text.encode()).hexdigest()
                    h2 = func(compare_text.encode()).hexdigest()
                    same = h1 == h2
                    st.markdown(
                        f"<div style='background:#f8f9fa;border-left:4px solid {color};"
                        f"border-radius:4px;padding:10px 14px;margin:6px 0'>"
                        f"<b style='color:{color}'>{name}</b> ({bits})<br>"
                        f"<code style='font-size:12px;word-break:break-all'>{h2}</code><br>"
                        f"<small style='color:{'#28a745' if same else '#dc3545'}'>"
                        f"{'✅ Hash SAMA' if same else '❌ Hash BERBEDA (Avalanche Effect)'}</small></div>",
                        unsafe_allow_html=True
                    )
 
        st.info(
            "💡 **Avalanche Effect**: Perubahan kecil pada input (bahkan 1 karakter) menghasilkan "
            "hash yang sama sekali berbeda. Ini adalah sifat penting fungsi hash kriptografi."
        )
 
 
st.markdown("---")
st.caption("Dibuat untuk tugas Struktur Data | Informatika UINSSC MMXXVI")
 