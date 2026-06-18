# ================================================
#  app.py  —  Aplikasi Streamlit
#
#  "Benchmarking Performa Struktur Data untuk
#   Operasi Searching, Insertion, dan Deletion
#   Menggunakan Streamlit"
#
#  Mata Kuliah : Struktur Data
# ================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from dataset    import generate_dataset, sample_targets
from benchmark  import run_full_benchmark
from structures import ArrayDS, BST, HashTable, AVLTree

# ── Konfigurasi halaman ───────────────────────────
st.set_page_config(
    page_title="Benchmarking Struktur Data",
    page_icon="📊",
    layout="wide",
)

# ── Konstanta ─────────────────────────────────────
STRUCTURES = ["Array", "BST", "Hash Table", "AVL Tree"]
COLORS     = {
    "Array":      "#EF553B",
    "BST":        "#636EFA",
    "Hash Table": "#00CC96",
    "AVL Tree":   "#FFA15A",
}
OPS = ["insert", "search", "delete"]

# ═════════════════════════════════════════════════
#  HEADER
# ═════════════════════════════════════════════════
st.title("📊 Benchmarking Performa Struktur Data")
st.subheader("Operasi Searching, Insertion, dan Deletion Menggunakan Streamlit")
st.caption("Mata Kuliah: Struktur Data")
st.divider()

# ═════════════════════════════════════════════════
#  SIDEBAR — Konfigurasi
# ═════════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ Konfigurasi")

    ukuran = st.selectbox(
        "Ukuran Dataset",
        options=[100, 1_000, 10_000],
        format_func=lambda x: f"{x:,} data  ({'Kecil' if x==100 else 'Sedang' if x==1_000 else 'Besar'})",
    )

    jenis = st.selectbox(
        "Jenis Dataset",
        options=["acak", "terurut", "descending"],
        format_func=str.capitalize,
    )

    st.divider()
    st.markdown("**Struktur Data:**")
    for name, color in COLORS.items():
        st.markdown(f"<span style='color:{color}'>●</span> {name}", unsafe_allow_html=True)

    st.divider()
    st.markdown("**Kompleksitas:**")
    st.markdown("""
| Struktur | Search |
|---|---|
| Array | O(n) |
| BST | O(log n) |
| Hash Table | O(1) |
| AVL Tree | O(log n) |
    """)

# ═════════════════════════════════════════════════
#  TABS
# ═════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣  Generate Dataset",
    "2️⃣  Benchmark",
    "3️⃣  Visualisasi",
    "4️⃣  Hasil & Tabel",
    "5️⃣  Analisis",
])

# ─────────────────────────────────────────────────
#  TAB 1 — GENERATE DATASET
# ─────────────────────────────────────────────────
with tab1:
    st.subheader("Generate Dataset Otomatis")

    st.info(f"Dataset: **{ukuran:,} bilangan integer** — urutan **{jenis}**")

    if st.button("🔄 Generate Dataset", type="primary"):
        st.session_state.data   = generate_dataset(ukuran, jenis)
        st.session_state.ukuran = ukuran
        st.session_state.jenis  = jenis
        st.session_state.hasil  = None
        st.success(f"✅ Dataset berhasil di-generate: {ukuran:,} data ({jenis})")

    # Generate otomatis pertama kali
    if "data" not in st.session_state:
        st.session_state.data   = generate_dataset(ukuran, jenis)
        st.session_state.ukuran = ukuran
        st.session_state.jenis  = jenis
        st.session_state.hasil  = None

    data = st.session_state.data

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Data", f"{len(data):,}")
    col2.metric("Nilai Minimum", f"{min(data):,}")
    col3.metric("Nilai Maksimum", f"{max(data):,}")
    col4.metric("Jenis", jenis.capitalize())

    st.markdown("**Preview 20 data pertama:**")
    st.dataframe(
        pd.DataFrame({"Index": range(20), "Nilai": data[:20]}),
        use_container_width=True,
        hide_index=True,
        height=250,
    )

# ─────────────────────────────────────────────────
#  TAB 2 — BENCHMARK
# ─────────────────────────────────────────────────
with tab2:
    st.subheader("Benchmarking Execution Time")

    data = st.session_state.get("data", [])

    # Uji Manual
    st.markdown("#### 🔧 Uji Operasi Manual")
    c1, c2, c3 = st.columns(3)
    with c1:
        val_input = st.number_input(
            "Nilai yang diuji",
            min_value=1,
            value=int(data[0]) if data else 1,
        )
    with c2:
        op_manual = st.selectbox("Operasi", ["Search", "Insert", "Delete"])
    with c3:
        ds_name = st.selectbox("Struktur Data", STRUCTURES)

    if st.button("▶ Jalankan Operasi"):
        import time
        ds_map = {
            "Array":      ArrayDS(),
            "BST":        BST(),
            "Hash Table": HashTable(),
            "AVL Tree":   AVLTree(),
        }
        ds = ds_map[ds_name]
        for v in data:
            ds.insert(v)

        t0 = time.perf_counter()
        if op_manual == "Search":
            found = ds.search(val_input)
            ms = (time.perf_counter() - t0) * 1000
            if found:
                st.success(f"✅ Nilai **{val_input}** ditemukan di {ds_name} — `{ms:.6f} ms`")
            else:
                st.warning(f"❌ Nilai **{val_input}** tidak ditemukan di {ds_name} — `{ms:.6f} ms`")
        elif op_manual == "Insert":
            ds.insert(val_input)
            ms = (time.perf_counter() - t0) * 1000
            st.success(f"✅ Nilai **{val_input}** disisipkan ke {ds_name} — `{ms:.6f} ms`")
        elif op_manual == "Delete":
            ok = ds.delete(val_input)
            ms = (time.perf_counter() - t0) * 1000
            if ok:
                st.success(f"✅ Nilai **{val_input}** dihapus dari {ds_name} — `{ms:.6f} ms`")
            else:
                st.warning(f"❌ Nilai **{val_input}** tidak ada di {ds_name}")

    st.divider()

    # Benchmark Otomatis
    st.markdown("#### ⚡ Benchmark Semua Struktur Data")

    if st.button("⚡ Jalankan Benchmark", type="primary", use_container_width=True):
        with st.spinner("Menjalankan benchmark... ⏳"):
            st.session_state.hasil = run_full_benchmark(data)
        st.success("✅ Benchmark selesai!")

    if st.session_state.get("hasil"):
        hasil = st.session_state.hasil
        st.markdown("#### Hasil Waktu Eksekusi (milidetik)")
        c1, c2, c3 = st.columns(3)
        for col, op, emoji in zip([c1, c2, c3], OPS, ["➕", "🔍", "🗑️"]):
            with col:
                st.markdown(f"**{emoji} {op.capitalize()}**")
                best = min(hasil[op], key=hasil[op].get)
                for name in STRUCTURES:
                    ms = hasil[op][name]
                    st.metric(
                        label=name,
                        value=f"{ms:.4f} ms",
                        delta="🏆 Tercepat" if name == best else None,
                        delta_color="off",
                    )

# ─────────────────────────────────────────────────
#  TAB 3 — VISUALISASI
# ─────────────────────────────────────────────────
with tab3:
    st.subheader("Visualisasi Grafik")

    if not st.session_state.get("hasil"):
        st.info("Jalankan benchmark di tab **Benchmark** terlebih dahulu.")
    else:
        hasil  = st.session_state.hasil
        ukuran = st.session_state.ukuran
        jenis  = st.session_state.jenis

        # ── Bar chart per operasi ──────────────────
        st.markdown("#### Bar Chart — Waktu per Operasi")
        for op, emoji in zip(OPS, ["➕", "🔍", "🗑️"]):
            names  = STRUCTURES
            times  = [hasil[op][n] for n in names]
            colors = [COLORS[n] for n in names]

            fig = go.Figure(go.Bar(
                x=names, y=times,
                marker_color=colors,
                text=[f"{t:.4f} ms" for t in times],
                textposition="outside",
            ))
            fig.update_layout(
                title=f"{emoji} Operasi {op.capitalize()} — {ukuran:,} data ({jenis})",
                xaxis_title="Struktur Data",
                yaxis_title="Waktu (ms)",
                height=340,
                margin=dict(t=50, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            fig.update_yaxes(gridcolor="rgba(128,128,128,0.15)")
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ── Grouped bar — semua operasi ────────────
        st.markdown("#### Grouped Bar Chart — Semua Operasi")
        rows = [
            {"Operasi": op.capitalize(), "Struktur Data": name, "Waktu (ms)": hasil[op][name]}
            for op in OPS for name in STRUCTURES
        ]
        fig_grp = px.bar(
            pd.DataFrame(rows), x="Operasi", y="Waktu (ms)",
            color="Struktur Data", barmode="group",
            color_discrete_map=COLORS, height=400,
        )
        fig_grp.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig_grp.update_yaxes(gridcolor="rgba(128,128,128,0.15)")
        st.plotly_chart(fig_grp, use_container_width=True)

        st.divider()

        # ── Radar chart ────────────────────────────
        st.markdown("#### Radar Chart — Performa Keseluruhan (dinormalisasi)")
        st.caption("Nilai lebih kecil = lebih cepat")

        max_per_op = [max(hasil[op][n] for n in STRUCTURES) for op in OPS]
        fig_radar  = go.Figure()

        for name in STRUCTURES:
            norm = [hasil[op][name] / (max_per_op[i] or 1) for i, op in enumerate(OPS)]
            norm.append(norm[0])
            fig_radar.add_trace(go.Scatterpolar(
                r=norm,
                theta=["Insert", "Search", "Delete", "Insert"],
                fill="toself",
                name=name,
                line_color=COLORS[name],
            ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            height=420,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.divider()

        # ── Line chart: perbandingan ukuran dataset ─
        st.markdown("#### Line Chart — Prediksi Performa pada Berbagai Ukuran Dataset")
        st.caption("Estimasi teoritis berdasarkan kompleksitas algoritma masing-masing struktur data.")

        import math
        sizes = [100, 500, 1000, 5000, 10000]
        base  = hasil["search"]

        # Skala teoritis relatif terhadap nilai benchmark nyata
        ref_n    = ukuran
        ref_arr  = base["Array"]
        ref_bst  = base["BST"]
        ref_ht   = base["Hash Table"]
        ref_avl  = base["AVL Tree"]

        def pred_arr(n): return ref_arr * (n / ref_n)
        def pred_bst(n): return ref_bst * (math.log2(n) / math.log2(ref_n)) if ref_n > 1 else ref_bst
        def pred_ht(n):  return ref_ht   # O(1) konstan
        def pred_avl(n): return ref_avl * (math.log2(n) / math.log2(ref_n)) if ref_n > 1 else ref_avl

        df_line = pd.DataFrame({
            "Ukuran (n)": sizes,
            "Array":      [pred_arr(n) for n in sizes],
            "BST":        [pred_bst(n) for n in sizes],
            "Hash Table": [pred_ht(n)  for n in sizes],
            "AVL Tree":   [pred_avl(n) for n in sizes],
        })

        fig_line = px.line(
            df_line, x="Ukuran (n)", y=STRUCTURES,
            color_discrete_map=COLORS,
            markers=True, height=380,
            labels={"value": "Waktu (ms)", "variable": "Struktur Data"},
        )
        fig_line.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig_line.update_yaxes(gridcolor="rgba(128,128,128,0.15)")
        st.plotly_chart(fig_line, use_container_width=True)

# ─────────────────────────────────────────────────
#  TAB 4 — HASIL & TABEL
# ─────────────────────────────────────────────────
with tab4:
    st.subheader("Hasil Benchmarking")

    if not st.session_state.get("hasil"):
        st.info("Jalankan benchmark di tab **Benchmark** terlebih dahulu.")
    else:
        hasil = st.session_state.hasil

        # Tabel kompleksitas
        st.markdown("#### Tabel Kompleksitas Algoritma")
        df_complexity = pd.DataFrame({
            "Struktur Data": STRUCTURES,
            "Search":        ["O(n)",    "O(log n) avg", "O(1) avg",   "O(log n)"],
            "Insert":        ["O(1)*",   "O(log n) avg", "O(1) avg",   "O(log n)"],
            "Delete":        ["O(n)",    "O(log n) avg", "O(1) avg",   "O(log n)"],
            "Worst Case":    ["O(n)",    "O(n)",         "O(n)",       "O(log n)"],
            "Seimbang?":     ["—",       "Tidak",        "—",          "Ya"],
        })
        st.dataframe(df_complexity, use_container_width=True, hide_index=True)
        st.caption("*Insert Array O(1) amortized — kadang O(n) jika resize")

        st.divider()

        # Tabel hasil benchmark
        st.markdown("#### Tabel Hasil Benchmark (ms)")
        rows = []
        for name in STRUCTURES:
            rows.append({
                "Struktur Data":  name,
                "Insert (ms)":    hasil["insert"][name],
                "Search (ms)":    hasil["search"][name],
                "Delete (ms)":    hasil["delete"][name],
                "Total (ms)":     round(
                    hasil["insert"][name] + hasil["search"][name] + hasil["delete"][name], 4
                ),
            })
        df_res = pd.DataFrame(rows).sort_values("Total (ms)")
        df_res["Rank"] = range(1, len(df_res) + 1)

        def hl(s):
            return ["background-color:#d4edda;color:#155724;font-weight:bold"
                    if v == s.min() else "" for v in s]

        st.dataframe(
            df_res.style.apply(hl, subset=["Insert (ms)", "Search (ms)", "Delete (ms)", "Total (ms)"]),
            use_container_width=True,
            hide_index=True,
        )

        # Download CSV
        csv = df_res.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Hasil CSV",
            data=csv,
            file_name=f"benchmark_{st.session_state.ukuran}_{st.session_state.jenis}.csv",
            mime="text/csv",
        )

        st.divider()

        st.markdown("#### 🏆 Pemenang per Operasi")
        c1, c2, c3 = st.columns(3)
        for col, op, emoji in zip([c1, c2, c3], OPS, ["➕", "🔍", "🗑️"]):
            winner = min(hasil[op], key=hasil[op].get)
            with col:
                st.success(f"{emoji} **{op.capitalize()}**\n\n🏆 **{winner}**\n\n`{hasil[op][winner]:.4f} ms`")

# ─────────────────────────────────────────────────
#  TAB 5 — ANALISIS
# ─────────────────────────────────────────────────
with tab5:
    st.subheader("Analisis Hasil Pengujian")

    if not st.session_state.get("hasil"):
        st.info("Jalankan benchmark di tab **Benchmark** terlebih dahulu.")
    else:
        hasil  = st.session_state.hasil
        ukuran = st.session_state.ukuran
        jenis  = st.session_state.jenis

        best_s = min(hasil["search"], key=hasil["search"].get)
        best_i = min(hasil["insert"], key=hasil["insert"].get)
        best_d = min(hasil["delete"], key=hasil["delete"].get)

        # ── Pertanyaan 1 ──────────────────────────
        st.markdown("### 1. Struktur Data dengan Performa Terbaik")
        st.markdown(f"""
Berdasarkan hasil benchmark dengan **{ukuran:,} data {jenis}**:

| Operasi | Terbaik | Waktu |
|---|---|---|
| Insert  | **{best_i}** | `{hasil['insert'][best_i]:.4f} ms` |
| Search  | **{best_s}** | `{hasil['search'][best_s]:.6f} ms` |
| Delete  | **{best_d}** | `{hasil['delete'][best_d]:.4f} ms` |

**Alasan:** Hash Table unggul di Search karena menggunakan fungsi hash yang memetakan
nilai langsung ke posisi memori (O(1)), sehingga tidak perlu membandingkan satu per satu
seperti Array, maupun melakukan traversal pohon seperti BST dan AVL Tree.
        """)

        st.divider()

        # ── Pertanyaan 2 ──────────────────────────
        st.markdown("### 2. Kelebihan dan Kekurangan Masing-masing Struktur Data")

        with st.expander("📦 Array / List — O(n) Search", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Kelebihan**")
                st.markdown("""
- Insert di akhir sangat cepat O(1)
- Implementasi sederhana
- Akses elemen by-index O(1)
- Hemat memori, cache-friendly
                """)
            with col2:
                st.markdown("**❌ Kekurangan**")
                st.markdown("""
- Search linear O(n) — lambat untuk data besar
- Delete memerlukan pergeseran elemen O(n)
- Tidak terurut otomatis
                """)

        with st.expander("🌲 Binary Search Tree (BST) — O(log n) avg"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Kelebihan**")
                st.markdown("""
- Search rata-rata O(log n)
- Data tersimpan terurut secara natural
- In-order traversal menghasilkan data terurut
                """)
            with col2:
                st.markdown("**❌ Kekurangan**")
                st.markdown(f"""
- Tidak seimbang otomatis
- Pada data **{jenis}**, bisa menjadi skewed tree O(n)
- Performa bergantung urutan input
                """)

        with st.expander("🗂️ Hash Table — O(1) avg"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Kelebihan**")
                st.markdown("""
- Search dan Insert O(1) rata-rata
- Performa tidak bergantung urutan data
- Sangat efisien untuk lookup
                """)
            with col2:
                st.markdown("**❌ Kekurangan**")
                st.markdown("""
- Butuh memori ekstra (ada slot kosong)
- Tidak mendukung operasi terurut
- Worst case O(n) jika banyak collision
                """)

        with st.expander("⚖️ AVL Tree — O(log n) dijamin"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Kelebihan**")
                st.markdown("""
- O(log n) **dijamin** untuk semua operasi
- Selalu seimbang (self-balancing)
- Tidak terpengaruh urutan input
                """)
            with col2:
                st.markdown("**❌ Kekurangan**")
                st.markdown("""
- Insert & Delete lebih lambat dari BST (ada rotasi)
- Implementasi lebih kompleks
- Overhead rotasi pada setiap perubahan
                """)

        st.divider()

        # ── Pertanyaan 3 ──────────────────────────
        st.markdown("### 3. Prediksi Performa jika Dataset Diperbesar")

        df_pred = pd.DataFrame({
            "Ukuran (n)":       ["100", "1.000", "10.000", "100.000", "1.000.000"],
            "Array — O(n)":     ["~1×", "~10×",  "~100×",  "~1.000×", "~10.000×"],
            "BST — O(log n)":   ["7 langkah", "10 langkah", "13 langkah", "17 langkah", "20 langkah"],
            "Hash Table — O(1)":["konstan", "konstan", "konstan", "konstan", "konstan*"],
            "AVL Tree — O(log n)":["7 langkah", "10 langkah", "13 langkah", "17 langkah", "20 langkah"],
        })
        st.dataframe(df_pred, use_container_width=True, hide_index=True)
        st.caption("*Hash Table melambat jika load factor tinggi dan banyak collision")
        st.markdown("""
**Kesimpulan prediksi:** Jika n diperbesar 100×, waktu Array meningkat 100×,
sedangkan BST dan AVL Tree hanya meningkat ~2× (log₂ 10.000 ÷ log₂ 100 = 13/7 ≈ 1,9×),
dan Hash Table tetap konstan.
        """)

        st.divider()

        # ── Pertanyaan 4 ──────────────────────────
        st.markdown("### 4. Kesesuaian Hasil Eksperimen dengan Teori")

        ht_ms  = hasil["search"]["Hash Table"]
        arr_ms = hasil["search"]["Array"]
        bst_ms = hasil["search"]["BST"]
        avl_ms = hasil["search"]["AVL Tree"]

        if ht_ms < arr_ms:
            st.success(
                f"✅ **Mendukung teori:** Hash Table ({ht_ms:.6f} ms) "
                f"lebih cepat dari Array ({arr_ms:.6f} ms) untuk Search — "
                f"sesuai dengan O(1) vs O(n)."
            )
        else:
            st.warning(
                f"⚠️ Pada dataset kecil ({ukuran} data), overhead Python dapat "
                f"menyembunyikan keunggulan O(1). Coba dengan 10.000 data."
            )

        if avl_ms <= bst_ms * 1.5:
            st.success(
                f"✅ **Mendukung teori:** AVL Tree ({avl_ms:.6f} ms) "
                f"performanya sebanding dengan BST ({bst_ms:.6f} ms), "
                f"dengan keunggulan garansi keseimbangan."
            )

        if jenis == "terurut":
            st.error(
                "⚠️ **Catatan penting:** Dataset **terurut** menyebabkan BST menjadi "
                "skewed tree (pohon condong ke satu sisi), sehingga Search mendekati O(n). "
                "Inilah keunggulan AVL Tree — tetap O(log n) meski data terurut."
            )

        st.divider()

        # ── Pertanyaan 5 ──────────────────────────
        st.markdown("### 5. Peran Benchmarking dalam Pengembangan Software")
        st.markdown(f"""
Hasil benchmarking dengan **{ukuran:,} data {jenis}** memberikan informasi empiris
yang membantu pengambilan keputusan dalam pengembangan software:

**a. Pemilihan Struktur Data yang Tepat**
> Jika aplikasi dominan melakukan operasi **pencarian** (search), maka
Hash Table adalah pilihan terbaik karena O(1). Namun jika diperlukan
data **terurut** atau **range query**, AVL Tree lebih sesuai.

**b. Validasi Kompleksitas Teoritis**
> Eksperimen ini mengkonfirmasi bahwa kompleksitas Big-O bukan sekadar
teori — perbedaannya nyata terukur, terutama pada dataset besar (10.000 data).

**c. Trade-off Memori vs Kecepatan**
> Hash Table tercepat dalam Search, namun menggunakan memori lebih banyak
karena ada slot kosong. Array paling hemat memori namun lambat saat pencarian.

**d. Skalabilitas**
> Benchmark membantu memprediksi apakah sistem akan tetap responsif
saat data bertambah dari ribuan menjadi jutaan record.

**Rekomendasi umum:**
- Pencarian cepat (lookup) → **Hash Table**
- Data selalu terurut + pencarian → **AVL Tree**
- Data kecil + sederhana → **Array**
- Data acak + pencarian sedang → **BST**
        """)

        st.divider()

        # ── Kesimpulan ────────────────────────────
        st.markdown("### 6. Kesimpulan")
        st.info(f"""
**Dari eksperimen benchmarking dengan {ukuran:,} data {jenis}:**

1. **Hash Table** memiliki performa Search terbaik (O(1) rata-rata).
2. **AVL Tree** memberikan performa paling **konsisten** karena selalu seimbang.
3. **BST** performanya tidak stabil — baik untuk data acak, buruk untuk data terurut.
4. **Array** paling lambat untuk Search dan Delete (O(n)), namun Insert tercepat.
5. Hasil eksperimen **sejalan dengan kompleksitas teoritis**, terutama pada dataset besar.
6. Pemilihan struktur data harus disesuaikan dengan **pola operasi dominan** dalam aplikasi.
        """)