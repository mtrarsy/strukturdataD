# MUH Haekal bilal, Putra Rais Hakim, Wulan Sari, MUH Aziz Susilo Purnomo

import streamlit as st
import time
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from collections import defaultdict
import sys
import traceback

sys.setrecursionlimit(20000)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DS Benchmark Lab",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS  (biru selaras dengan slide)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A3A8C 0%, #0D2260 100%);
    color: #fff;
}
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] .stRadio > label { font-weight: 700; letter-spacing:.05em; }

/* main bg */
.main .block-container { padding-top: 1.5rem; max-width: 1100px; }

/* hero */
.hero {
    background: linear-gradient(135deg, #1A3A8C 0%, #2756D4 60%, #3B82F6 100%);
    border-radius: 18px;
    padding: 3rem 2.5rem 2.5rem;
    color: #fff;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.hero::after {
    content: "🌳";
    position: absolute; right: 2.5rem; top: 1.5rem;
    font-size: 6rem; opacity: .15;
}
.hero h1 { font-size: 2.6rem; font-weight: 900; margin: 0 0 .4rem; letter-spacing: -.02em; }
.hero p  { font-size: 1.05rem; opacity: .85; margin: 0; }

/* card */
.card {
    background: #fff;
    border: 1.5px solid #E5EAF5;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 12px rgba(26,58,140,.07);
}
.card h3 { color: #1A3A8C; margin: 0 0 .5rem; font-weight: 700; }

/* metric pill */
.pill {
    display: inline-block;
    background: #EEF3FF;
    color: #1A3A8C;
    border-radius: 999px;
    padding: .25rem .8rem;
    font-weight: 700;
    font-size: .85rem;
    margin: .15rem .15rem 0 0;
}

/* section title */
.sec-title {
    font-size: 1.4rem; font-weight: 800; color: #1A3A8C;
    border-left: 5px solid #2756D4;
    padding-left: .75rem;
    margin: 1.5rem 0 1rem;
}

/* step badge */
.step {
    display: inline-block;
    background: #2756D4; color: #fff;
    border-radius: 999px;
    width: 28px; height: 28px;
    text-align: center; line-height: 28px;
    font-weight: 800; font-size: .85rem;
    margin-right: .5rem;
}

/* result table */
table { width:100%; border-collapse:collapse; font-size:.9rem; }
th { background:#1A3A8C; color:#fff; padding:.6rem .9rem; text-align:left; }
td { padding:.55rem .9rem; border-bottom:1px solid #E5EAF5; }
tr:hover td { background:#F0F5FF; }

/* info box */
.info-box {
    background: #EEF3FF; border-left: 4px solid #2756D4;
    border-radius: 0 10px 10px 0;
    padding: .9rem 1.1rem; margin: .8rem 0;
    font-size: .93rem; color: #1A3A8C;
}

/* alert */
.warn-box {
    background: #FFF7E6; border-left: 4px solid #F59E0B;
    border-radius: 0 10px 10px 0;
    padding: .9rem 1.1rem; margin: .8rem 0;
    font-size: .93rem; color: #92400E;
}

/* end page */
.end-hero {
    background: linear-gradient(135deg, #0D2260 0%, #1A3A8C 50%, #2756D4 100%);
    border-radius: 18px;
    padding: 4rem 2.5rem;
    text-align: center;
    color: #fff;
}
.end-hero h1 { font-size: 3rem; font-weight: 900; }
.end-hero p { opacity: .8; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────

# ── Array / List ──────────────────────────────
class ArrayDS:
    def __init__(self): self.data = []
    def insert(self, v): self.data.append(v)
    def search(self, v): return v in self.data
    def delete(self, v):
        try: self.data.remove(v)
        except ValueError: pass
    def reset(self): self.data = []

# ── Hash Table ────────────────────────────────
class HashTableDS:
    def __init__(self): self.data = {}
    def insert(self, v): self.data[v] = True
    def search(self, v): return v in self.data
    def delete(self, v): self.data.pop(v, None)
    def reset(self): self.data = {}

# ── BST ───────────────────────────────────────
class BSTNode:
    def __init__(self, v): self.val = v; self.left = self.right = None

class BST:
    def __init__(self): self.root = None
    def insert(self, v): self.root = self._ins(self.root, v)
    def _ins(self, node, v):
        if not node: return BSTNode(v)
        if v < node.val: node.left  = self._ins(node.left,  v)
        elif v > node.val: node.right = self._ins(node.right, v)
        return node
    def search(self, v):
        n = self.root
        while n:
            if v == n.val: return True
            n = n.left if v < n.val else n.right
        return False
    def delete(self, v): self.root = self._del(self.root, v)
    def _del(self, node, v):
        if not node: return None
        if v < node.val: node.left  = self._del(node.left,  v)
        elif v > node.val: node.right = self._del(node.right, v)
        else:
            if not node.left:  return node.right
            if not node.right: return node.left
            m = node.right
            while m.left: m = m.left
            node.val = m.val; node.right = self._del(node.right, m.val)
        return node
    def reset(self): self.root = None

# ── AVL Tree ──────────────────────────────────
class AVLNode:
    def __init__(self, v): self.val = v; self.left = self.right = None; self.h = 1

class AVLTree:
    def __init__(self): self.root = None
    def _h(self, n): return n.h if n else 0
    def _bf(self, n): return self._h(n.left) - self._h(n.right) if n else 0
    def _upd(self, n): n.h = 1 + max(self._h(n.left), self._h(n.right))
    def _rr(self, z):
        y = z.left; T3 = y.right
        y.right = z; z.left = T3
        self._upd(z); self._upd(y); return y
    def _lr(self, z):
        y = z.right; T2 = y.left
        y.left = z; z.right = T2
        self._upd(z); self._upd(y); return y
    def _bal(self, n):
        self._upd(n); bf = self._bf(n)
        if bf > 1:
            if self._bf(n.left) < 0: n.left = self._lr(n.left)
            return self._rr(n)
        if bf < -1:
            if self._bf(n.right) > 0: n.right = self._rr(n.right)
            return self._lr(n)
        return n
    def insert(self, v): self.root = self._ins(self.root, v)
    def _ins(self, n, v):
        if not n: return AVLNode(v)
        if v < n.val: n.left  = self._ins(n.left,  v)
        elif v > n.val: n.right = self._ins(n.right, v)
        return self._bal(n)
    def search(self, v):
        n = self.root
        while n:
            if v == n.val: return True
            n = n.left if v < n.val else n.right
        return False
    def delete(self, v): self.root = self._del(self.root, v)
    def _del(self, n, v):
        if not n: return None
        if v < n.val: n.left  = self._del(n.left,  v)
        elif v > n.val: n.right = self._del(n.right, v)
        else:
            if not n.left: return n.right
            if not n.right: return n.left
            m = n.right
            while m.left: m = m.left
            n.val = m.val; n.right = self._del(n.right, m.val)
        return self._bal(n)
    def reset(self): self.root = None

# ── Red-Black Tree ────────────────────────────
RED, BLACK = True, False

class RBNode:
    def __init__(self, v):
        self.val = v; self.color = RED
        self.left = self.right = self.parent = None

class RBTree:
    def __init__(self):
        self.NIL = RBNode(None); self.NIL.color = BLACK
        self.root = self.NIL
    def _lr(self, x):
        y = x.right; x.right = y.left
        if y.left != self.NIL: y.left.parent = x
        y.parent = x.parent
        if not x.parent: self.root = y
        elif x == x.parent.left: x.parent.left = y
        else: x.parent.right = y
        y.left = x; x.parent = y
    def _rr(self, x):
        y = x.left; x.left = y.right
        if y.right != self.NIL: y.right.parent = x
        y.parent = x.parent
        if not x.parent: self.root = y
        elif x == x.parent.right: x.parent.right = y
        else: x.parent.left = y
        y.right = x; x.parent = y
    def insert(self, v):
        z = RBNode(v); z.left = z.right = z.parent = self.NIL
        y = None; x = self.root
        while x != self.NIL:
            y = x; x = x.left if z.val < x.val else x.right
        z.parent = y
        if not y: self.root = z
        elif z.val < y.val: y.left = z
        else: y.right = z
        self._fix_ins(z)
    def _fix_ins(self, z):
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                u = z.parent.parent.right
                if u.color == RED:
                    z.parent.color = BLACK; u.color = BLACK
                    z.parent.parent.color = RED; z = z.parent.parent
                else:
                    if z == z.parent.right: z = z.parent; self._lr(z)
                    z.parent.color = BLACK; z.parent.parent.color = RED
                    self._rr(z.parent.parent)
            else:
                u = z.parent.parent.left
                if u.color == RED:
                    z.parent.color = BLACK; u.color = BLACK
                    z.parent.parent.color = RED; z = z.parent.parent
                else:
                    if z == z.parent.left: z = z.parent; self._rr(z)
                    z.parent.color = BLACK; z.parent.parent.color = RED
                    self._lr(z.parent.parent)
        self.root.color = BLACK
    def search(self, v):
        n = self.root
        while n != self.NIL:
            if v == n.val: return True
            n = n.left if v < n.val else n.right
        return False
    def delete(self, v):
        z = self.root
        while z != self.NIL:
            if v == z.val: break
            z = z.left if v < z.val else z.right
        if z == self.NIL: return
        self._del(z)
    def _del(self, z):
        y = z; yoc = y.color; NIL = self.NIL
        if z.left == NIL: x = z.right; self._trans(z, z.right)
        elif z.right == NIL: x = z.left; self._trans(z, z.left)
        else:
            y = z.right
            while y.left != NIL: y = y.left
            yoc = y.color; x = y.right
            if y.parent == z: x.parent = y
            else:
                self._trans(y, y.right); y.right = z.right; y.right.parent = y
            self._trans(z, y); y.left = z.left; y.left.parent = y; y.color = z.color
        if yoc == BLACK: self._fix_del(x)
    def _trans(self, u, v):
        if not u.parent: self.root = v
        elif u == u.parent.left: u.parent.left = v
        else: u.parent.right = v
        v.parent = u.parent
    def _fix_del(self, x):
        NIL = self.NIL
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK; x.parent.color = RED; self._lr(x.parent); w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED; x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK; w.color = RED; self._rr(w); w = x.parent.right
                    w.color = x.parent.color; x.parent.color = BLACK
                    w.right.color = BLACK; self._lr(x.parent); x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK; x.parent.color = RED; self._rr(x.parent); w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED; x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK; w.color = RED; self._lr(w); w = x.parent.left
                    w.color = x.parent.color; x.parent.color = BLACK
                    w.left.color = BLACK; self._rr(x.parent); x = self.root
        x.color = BLACK
    def reset(self):
        self.NIL = RBNode(None); self.NIL.color = BLACK; self.root = self.NIL

# ─────────────────────────────────────────────
# DATASET GENERATOR  (BARU)
# ─────────────────────────────────────────────
def generate_dataset(size, jenis):
    """
    Membuat dataset sesuai jenis yang dipilih:
    - "Acak"       -> urutan dikacau secara random (random.shuffle)
    - "Terurut"    -> urutan menaik (ascending)
    - "Descending" -> urutan menurun (descending)
    """
    base = list(range(size))
    if jenis == "Acak":
        data = base.copy()
        random.shuffle(data)
        return data
    elif jenis == "Terurut":
        return base  # sudah menaik (0,1,2,...,size-1)
    elif jenis == "Descending":
        return base[::-1]  # menurun (size-1,...,1,0)
    else:
        data = base.copy()
        random.shuffle(data)
        return data


DATASET_TYPES_ALL = ["Acak", "Terurut", "Descending"]
DATASET_ICON = {"Acak": "🎲", "Terurut": "📈", "Descending": "📉"}


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "bench_done" not in st.session_state:
        st.session_state.bench_done = False

init_state()

# ─────────────────────────────────────────────
# SIDEBAR NAV
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌳 DS Benchmark Lab")
    st.markdown("---")
    pages = [
        "🏠 Home",
        "🗂️ Struktur Data",
        "⚙️ Pilih Operasi",
        "🚀 Benchmark",
        "📊 Grafik",
        "👋 End",
    ]
    for p in pages:
        active = "→ " if st.session_state.page == p else "   "
        if st.button(f"{active}{p}", key=f"nav_{p}", use_container_width=True):
            st.session_state.page = p
            st.rerun()
    st.markdown("---")
    st.markdown("""
    <div style='font-size:.78rem; opacity:.7; line-height:1.7'>
    📘 Materi: Balanced Binary Tree<br>
    🏫 Informatika UINSSC<br>
    👨‍🏫 Muhammad Iszul Wilsa
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
if st.session_state.page == "🏠 Home":
    st.markdown("""
    <div class='hero'>
        <h1>Data Structure<br>Benchmark Lab</h1>
        <p>Struktur Data · Informatika UINSSC MMXXVI · Muhammad Iszul Wilsa, S.Si., M.Cs</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class='card'>
            <h3>🌳 Balanced Trees</h3>
            <p style='color:#555;font-size:.9rem'>AVL Tree, Red-Black Tree, BST – pelajari perbedaan struktur dan performa tiap pohon biner.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='card'>
            <h3>⚡ Benchmark Nyata</h3>
            <p style='color:#555;font-size:.9rem'>Ukur waktu eksekusi Insert, Search, dan Delete pada berbagai ukuran & jenis dataset (acak, terurut, descending) secara langsung.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class='card'>
            <h3>📊 Visualisasi</h3>
            <p style='color:#555;font-size:.9rem'>Bandingkan kompleksitas waktu antar struktur data melalui grafik interaktif yang mudah dibaca.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>Panduan Penggunaan</div>", unsafe_allow_html=True)
    steps = [
        ("🗂️ Struktur Data", "Pelajari deskripsi tiap struktur data yang tersedia."),
        ("⚙️ Pilih Operasi", "Tentukan operasi (Insert/Search/Delete), jenis dataset (acak/terurut/descending), dan ukuran data."),
        ("🚀 Benchmark", "Jalankan benchmark dan lihat hasil waktu eksekusi."),
        ("📊 Grafik", "Bandingkan performa melalui grafik bar & line."),
        ("👋 End", "Kesimpulan dan informasi Project UAS."),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""
        <div class='card' style='display:flex;align-items:center;gap:1rem;padding:.9rem 1.2rem'>
            <span class='step'>{i}</span>
            <div><strong style='color:#1A3A8C'>{title}</strong>
            <span style='color:#555;font-size:.88rem'> — {desc}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("▶  Mulai Sekarang", type="primary", use_container_width=False):
        st.session_state.page = "🗂️ Struktur Data"; st.rerun()

# ─────────────────────────────────────────────
# PAGE: STRUKTUR DATA
# ─────────────────────────────────────────────
elif st.session_state.page == "🗂️ Struktur Data":
    st.markdown("<div class='sec-title'>🗂️ Struktur Data yang Tersedia</div>", unsafe_allow_html=True)

    ds_info = {
        "Array / List": {
            "icon": "📋",
            "desc": "Koleksi elemen berurutan yang disimpan di memori kontigu.",
            "insert": "O(1) amortized",
            "search": "O(n)",
            "delete": "O(n)",
            "note": "Sederhana, cepat untuk append, lambat untuk pencarian & hapus.",
            "color": "#EEF3FF",
        },
        "Hash Table": {
            "icon": "🗝️",
            "desc": "Struktur berbasis fungsi hash untuk akses O(1) rata-rata.",
            "insert": "O(1) avg",
            "search": "O(1) avg",
            "delete": "O(1) avg",
            "note": "Tercepat rata-rata, namun tidak menjaga urutan dan worst-case O(n).",
            "color": "#F0FFF4",
        },
        "BST": {
            "icon": "🌿",
            "desc": "Binary Search Tree: setiap node kiri < root < kanan.",
            "insert": "O(log n) avg",
            "search": "O(log n) avg",
            "delete": "O(log n) avg",
            "note": "Bisa terdegradasi ke O(n) jika data dimasukkan secara terurut/descending (tidak seimbang).",
            "color": "#FFFBEB",
        },
        "AVL Tree": {
            "icon": "⚖️",
            "desc": "Self-balancing BST. Balance Factor tiap node: −1 ≤ BF ≤ 1.",
            "insert": "O(log n)",
            "search": "O(log n)",
            "delete": "O(log n)",
            "note": "Selalu seimbang dengan rotasi otomatis (LL, RR, LR, RL), performa stabil di semua jenis dataset.",
            "color": "#EEF3FF",
        },
        "Red-Black Tree": {
            "icon": "🔴⚫",
            "desc": "Self-balancing BST dengan properti warna merah/hitam pada setiap node.",
            "insert": "O(log n)",
            "search": "O(log n)",
            "delete": "O(log n)",
            "note": "Lebih sedikit rotasi dibanding AVL, cocok untuk banyak insert/delete.",
            "color": "#FFF1F1",
        },
    }

    for name, info in ds_info.items():
        with st.expander(f"{info['icon']}  {name}", expanded=False):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"<div class='info-box'>{info['desc']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='warn-box'>💡 {info['note']}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class='card' style='background:{info["color"]}'>
                    <h3 style='font-size:.95rem;margin-bottom:.6rem'>Kompleksitas Waktu</h3>
                    <div><span class='pill'>Insert {info['insert']}</span></div>
                    <div><span class='pill'>Search {info['search']}</span></div>
                    <div><span class='pill'>Delete {info['delete']}</span></div>
                </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
    💡 <strong>Jenis Dataset Pengujian:</strong><br>
    🎲 <strong>Acak</strong> — elemen disusun dalam urutan acak (random.shuffle).<br>
    📈 <strong>Terurut</strong> — elemen disusun menaik dari nilai terkecil ke terbesar.<br>
    📉 <strong>Descending</strong> — elemen disusun menurun dari nilai terbesar ke terkecil.
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Lanjut ke Pilih Operasi →", type="primary"):
        st.session_state.page = "⚙️ Pilih Operasi"; st.rerun()

# ─────────────────────────────────────────────
# PAGE: PILIH OPERASI
# ─────────────────────────────────────────────
elif st.session_state.page == "⚙️ Pilih Operasi":
    st.markdown("<div class='sec-title'>⚙️ Konfigurasi Benchmark</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🌳 Pilih Struktur Data")
        ds_choices = st.multiselect(
            "Struktur Data",
            ["Array / List", "Hash Table", "BST", "AVL Tree", "Red-Black Tree"],
            default=["Array / List", "Hash Table", "AVL Tree", "Red-Black Tree"],
            label_visibility="collapsed",
        )

        st.markdown("#### ⚡ Pilih Operasi")
        ops = st.multiselect(
            "Operasi",
            ["Insert", "Search", "Delete"],
            default=["Insert", "Search", "Delete"],
            label_visibility="collapsed",
        )

        st.markdown("#### 🔀 Jenis Dataset")
        dataset_types = st.multiselect(
            "Jenis Dataset",
            DATASET_TYPES_ALL,
            default=DATASET_TYPES_ALL,
            label_visibility="collapsed",
            help="Acak = random.shuffle · Terurut = menaik (ascending) · Descending = menurun",
        )

    with c2:
        st.markdown("#### 📏 Ukuran Data")
        sizes_preset = st.selectbox("Preset ukuran", [
            "Kecil (100 – 1 000)",
            "Sedang (500 – 5 000)",
            "Besar (1 000 – 10 000)",
            "Custom",
        ])
        if sizes_preset == "Kecil (100 – 1 000)":
            sizes = [100, 250, 500, 750, 1000]
        elif sizes_preset == "Sedang (500 – 5 000)":
            sizes = [500, 1000, 2000, 3500, 5000]
        elif sizes_preset == "Besar (1 000 – 10 000)":
            sizes = [1000, 2500, 5000, 7500, 10000]
        else:
            raw = st.text_input("Masukkan ukuran dipisah koma", "100,500,1000,5000")
            try:
                sizes = [int(x.strip()) for x in raw.split(",") if x.strip()]
            except:
                sizes = [100, 500, 1000]

        st.markdown("#### 🔁 Jumlah Ulangan")
        repeat = st.slider("Ulangan per ukuran", 1, 5, 3)

        if max(sizes, default=0) >= 5000 and any(d in ("Terurut", "Descending") for d in dataset_types):
            st.markdown("""<div class='warn-box'>
            ⚠️ Dataset <strong>Terurut</strong>/<strong>Descending</strong> berukuran besar dapat membuat
            <strong>BST</strong> sangat lambat (mendekati O(n²)) karena pohon menjadi tidak seimbang
            (degenerate tree). Proses benchmark mungkin memerlukan waktu cukup lama.
            </div>""", unsafe_allow_html=True)

    if ds_choices and ops and dataset_types:
        st.session_state.config = {
            "ds": ds_choices, "ops": ops,
            "sizes": sizes, "repeat": repeat,
            "dataset_types": dataset_types,
        }
        st.markdown(f"""
        <div class='card' style='background:#EEF3FF'>
            <h3>Ringkasan Konfigurasi</h3>
            <span class='pill'>Struktur: {len(ds_choices)}</span>
            <span class='pill'>Operasi: {', '.join(ops)}</span>
            <span class='pill'>Jenis Dataset: {', '.join(dataset_types)}</span>
            <span class='pill'>Ukuran: {sizes}</span>
            <span class='pill'>Ulangan: {repeat}×</span>
        </div>""", unsafe_allow_html=True)

        if st.button("▶  Jalankan Benchmark →", type="primary"):
            st.session_state.page = "🚀 Benchmark"; st.rerun()
    else:
        st.warning("Pilih minimal 1 struktur data, 1 operasi, dan 1 jenis dataset.")

# ─────────────────────────────────────────────
# PAGE: BENCHMARK
# ─────────────────────────────────────────────
elif st.session_state.page == "🚀 Benchmark":
    st.markdown("<div class='sec-title'>🚀 Jalankan Benchmark</div>", unsafe_allow_html=True)

    if "config" not in st.session_state:
        st.warning("⚠️ Konfigurasi belum diatur. Kembali ke Pilih Operasi.")
        if st.button("← Kembali"): st.session_state.page = "⚙️ Pilih Operasi"; st.rerun()
    else:
        cfg = st.session_state.config

        DS_MAP = {
            "Array / List": ArrayDS,
            "Hash Table": HashTableDS,
            "BST": BST,
            "AVL Tree": AVLTree,
            "Red-Black Tree": RBTree,
        }

        def bench_one(DSClass, op, size, repeat, jenis_dataset):
            """
            Mengukur rata-rata waktu eksekusi (ms) untuk satu kombinasi
            struktur data, operasi, ukuran data, dan jenis dataset
            (Acak / Terurut / Descending).
            """
            times = []
            for _ in range(repeat):
                ds = DSClass()
                data = generate_dataset(size, jenis_dataset)
                # pre-insert untuk operasi search/delete
                if op in ("Search", "Delete"):
                    for v in data: ds.insert(v)
                t0 = time.perf_counter()
                if op == "Insert":
                    for v in data: ds.insert(v)
                elif op == "Search":
                    for v in data: ds.search(v)
                else:
                    for v in data: ds.delete(v)
                times.append((time.perf_counter() - t0) * 1000)
            return round(np.mean(times), 4)

        run_btn = st.button("▶  Mulai Benchmark", type="primary")

        if run_btn or st.session_state.bench_done:
            if run_btn:
                st.session_state.bench_done = False
                results = defaultdict(dict)
                total = (len(cfg["ds"]) * len(cfg["ops"])
                         * len(cfg["sizes"]) * len(cfg["dataset_types"]))
                bar = st.progress(0, text="Memulai…")
                step = 0

                for ds_name in cfg["ds"]:
                    for jenis in cfg["dataset_types"]:
                        for op in cfg["ops"]:
                            for sz in cfg["sizes"]:
                                bar.progress(step / total,
                                    text=f"[{ds_name}] {jenis} · {op} · n={sz:,}")
                                try:
                                    t = bench_one(DS_MAP[ds_name], op, sz, cfg["repeat"], jenis)
                                except RecursionError:
                                    t = None
                                results[ds_name][f"{jenis}_{op}_{sz}"] = t
                                step += 1
                bar.progress(1.0, text="✅ Selesai!")
                st.session_state.results = dict(results)
                st.session_state.bench_done = True

            # ── Display results table ──
            results = st.session_state.results

            for jenis in cfg["dataset_types"]:
                st.markdown(
                    f"<div class='sec-title'>{DATASET_ICON.get(jenis,'')} Jenis Dataset: {jenis}</div>",
                    unsafe_allow_html=True)

                for op in cfg["ops"]:
                    st.markdown(f"<div class='sec-title' style='font-size:1.1rem'>Operasi: {op}</div>",
                                unsafe_allow_html=True)
                    rows = ""
                    header = "<tr><th>Struktur Data</th>" + "".join(
                        f"<th>n = {s:,}</th>" for s in cfg["sizes"]) + "</tr>"
                    for ds_name in cfg["ds"]:
                        row = f"<tr><td><strong>{ds_name}</strong></td>"
                        for sz in cfg["sizes"]:
                            val = results.get(ds_name, {}).get(f"{jenis}_{op}_{sz}", "-")
                            if val is None:
                                row += "<td>⚠️ RecursionError</td>"
                            else:
                                row += f"<td>{val} ms</td>"
                        row += "</tr>"
                        rows += row
                    st.markdown(f"<table>{header}{rows}</table>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Lihat Grafik →", type="primary"):
                st.session_state.page = "📊 Grafik"; st.rerun()

# ─────────────────────────────────────────────
# PAGE: GRAFIK
# ─────────────────────────────────────────────
elif st.session_state.page == "📊 Grafik":
    st.markdown("<div class='sec-title'>📊 Visualisasi Performa</div>", unsafe_allow_html=True)

    if not st.session_state.bench_done or not st.session_state.results:
        st.warning("⚠️ Belum ada data benchmark. Jalankan benchmark terlebih dahulu.")
        if st.button("← Ke Benchmark"): st.session_state.page = "🚀 Benchmark"; st.rerun()
    else:
        results = st.session_state.results
        cfg = st.session_state.config

        COLORS = {
            "Array / List":    "#2756D4",
            "Hash Table":      "#10B981",
            "BST":             "#F59E0B",
            "AVL Tree":        "#8B5CF6",
            "Red-Black Tree":  "#EF4444",
        }
        MARKERS = {
            "Array / List":    "o",
            "Hash Table":      "s",
            "BST":             "^",
            "AVL Tree":        "D",
            "Red-Black Tree":  "P",
        }

        c1, c2 = st.columns(2)
        with c1:
            chart_type = st.radio("Tipe Grafik", ["Line Chart", "Bar Chart", "Keduanya"],
                                   horizontal=True)
        with c2:
            jenis_pilih = st.selectbox(
                "🔀 Jenis Dataset yang Ditampilkan",
                cfg["dataset_types"],
                format_func=lambda j: f"{DATASET_ICON.get(j,'')} {j}",
            )

        for op in cfg["ops"]:
            st.markdown(f"#### Operasi: {op} — Dataset {jenis_pilih}")
            sizes = cfg["sizes"]
            fig, axes = plt.subplots(1, 2 if chart_type == "Keduanya" else 1,
                                     figsize=(14 if chart_type == "Keduanya" else 7, 4))
            if chart_type != "Keduanya":
                axes = [axes]

            ax_idx = 0
            if chart_type in ("Line Chart", "Keduanya"):
                ax = axes[ax_idx]; ax_idx += 1
                for ds_name in cfg["ds"]:
                    times = [results.get(ds_name, {}).get(f"{jenis_pilih}_{op}_{s}", 0) or 0 for s in sizes]
                    ax.plot(sizes, times,
                            marker=MARKERS.get(ds_name, "o"),
                            color=COLORS.get(ds_name, "#888"),
                            linewidth=2.2, markersize=7, label=ds_name)
                ax.set_title(f"Line Chart – {op} ({jenis_pilih})", fontweight="bold", color="#1A3A8C")
                ax.set_xlabel("Ukuran Data (n)"); ax.set_ylabel("Waktu (ms)")
                ax.legend(fontsize=8); ax.grid(True, alpha=.3)
                ax.set_facecolor("#FAFBFF")

            if chart_type in ("Bar Chart", "Keduanya"):
                ax = axes[ax_idx]
                x = np.arange(len(sizes)); w = 0.8 / max(len(cfg["ds"]), 1)
                for i, ds_name in enumerate(cfg["ds"]):
                    times = [results.get(ds_name, {}).get(f"{jenis_pilih}_{op}_{s}", 0) or 0 for s in sizes]
                    ax.bar(x + i * w, times, w * 0.9,
                           label=ds_name, color=COLORS.get(ds_name, "#888"), alpha=.85)
                ax.set_xticks(x + w * (len(cfg["ds"]) - 1) / 2)
                ax.set_xticklabels([f"n={s:,}" for s in sizes], fontsize=8)
                ax.set_title(f"Bar Chart – {op} ({jenis_pilih})", fontweight="bold", color="#1A3A8C")
                ax.set_xlabel("Ukuran Data (n)"); ax.set_ylabel("Waktu (ms)")
                ax.legend(fontsize=8); ax.grid(axis="y", alpha=.3)
                ax.set_facecolor("#FAFBFF")

            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        # ── Heatmap ringkasan ──
        st.markdown(f"#### 🗺️ Heatmap Performa (ms) — n terbesar, Dataset {jenis_pilih}")
        biggest = cfg["sizes"][-1]
        ds_list = cfg["ds"]; op_list = cfg["ops"]
        matrix = np.array([
            [results.get(ds, {}).get(f"{jenis_pilih}_{op}_{biggest}", 0) or 0 for op in op_list]
            for ds in ds_list
        ], dtype=float)

        fig2, ax2 = plt.subplots(figsize=(max(4, len(op_list)*2.5), max(3, len(ds_list)*0.9)))
        im = ax2.imshow(matrix, cmap="Blues", aspect="auto")
        ax2.set_xticks(range(len(op_list))); ax2.set_xticklabels(op_list, fontweight="bold")
        ax2.set_yticks(range(len(ds_list))); ax2.set_yticklabels(ds_list)
        for i in range(len(ds_list)):
            for j in range(len(op_list)):
                ax2.text(j, i, f"{matrix[i,j]:.2f}", ha="center", va="center",
                         fontsize=9, color="white" if matrix[i,j] > matrix.max()*.6 else "#1A3A8C")
        ax2.set_title(f"Waktu (ms) · n = {biggest:,} · Dataset {jenis_pilih}", fontweight="bold", color="#1A3A8C")
        fig2.colorbar(im, ax=ax2, label="ms"); fig2.tight_layout()
        st.pyplot(fig2); plt.close(fig2)

        # ── Perbandingan antar jenis dataset (BARU) ──
        if len(cfg["dataset_types"]) > 1:
            st.markdown("#### 🔀 Perbandingan Antar Jenis Dataset (n terbesar)")
            op_cmp = st.selectbox("Pilih Operasi untuk Dibandingkan", cfg["ops"], key="cmp_op")
            fig3, ax3 = plt.subplots(figsize=(8, 4))
            x = np.arange(len(cfg["dataset_types"])); w = 0.8 / max(len(ds_list), 1)
            for i, ds_name in enumerate(ds_list):
                vals = [results.get(ds_name, {}).get(f"{j}_{op_cmp}_{biggest}", 0) or 0
                        for j in cfg["dataset_types"]]
                ax3.bar(x + i * w, vals, w * 0.9, label=ds_name,
                        color=COLORS.get(ds_name, "#888"), alpha=.85)
            ax3.set_xticks(x + w * (len(ds_list) - 1) / 2)
            ax3.set_xticklabels(cfg["dataset_types"])
            ax3.set_title(f"{op_cmp} · n = {biggest:,} — Acak vs Terurut vs Descending",
                          fontweight="bold", color="#1A3A8C")
            ax3.set_ylabel("Waktu (ms)")
            ax3.legend(fontsize=8); ax3.grid(axis="y", alpha=.3)
            ax3.set_facecolor("#FAFBFF")
            fig3.tight_layout()
            st.pyplot(fig3); plt.close(fig3)
            st.markdown("""<div class='info-box'>
            💡 Grafik ini memperlihatkan sensitivitas tiap struktur data terhadap urutan data input.
            <strong>BST</strong> biasanya jauh lebih lambat pada dataset <strong>Terurut</strong>/<strong>Descending</strong>
            dibanding <strong>Acak</strong> karena pohon menjadi tidak seimbang (degenerate tree),
            sedangkan <strong>AVL Tree</strong>, <strong>Red-Black Tree</strong>, dan <strong>Hash Table</strong>
            relatif stabil di ketiga jenis dataset.
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Lihat Kesimpulan →", type="primary"):
            st.session_state.page = "👋 End"; st.rerun()

# ─────────────────────────────────────────────
# PAGE: END
# ─────────────────────────────────────────────
elif st.session_state.page == "👋 End":
    st.markdown("""
    <div class='end-hero'>
        <div style='font-size:4rem'>🌳</div>
        <h1>Terima Kasih!</h1>
        <p>Struktur Data · Informatika UINSSC · MMXXVI</p>
        <p style='margin-top:.5rem'>Presented by <strong>Muhammad Iszul Wilsa, S.Si., M.Cs</strong></p>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>📝 Kesimpulan</div>", unsafe_allow_html=True)
    concs = [
        ("Hash Table", "Tercepat rata-rata O(1) untuk semua operasi, ideal jika urutan tidak penting. Performa stabil di dataset acak, terurut, maupun descending."),
        ("AVL Tree", "Selalu seimbang → O(log n) terjamin pada dataset acak, terurut, maupun descending, cocok untuk banyak pencarian."),
        ("Red-Black Tree", "Lebih sedikit rotasi daripada AVL, unggul saat banyak Insert/Delete, performa relatif stabil di berbagai jenis dataset."),
        ("BST", "Performa bergantung urutan input; pada dataset acak mendekati O(log n), tetapi pada dataset terurut/descending bisa terdegradasi menjadi O(n) bahkan O(n²)."),
        ("Array / List", "Sederhana dan cache-friendly, tetapi Search & Delete O(n) — tidak dipengaruhi jenis dataset."),
    ]
    for ds, txt in concs:
        st.markdown(f"""
        <div class='card' style='display:flex;gap:1rem;align-items:flex-start'>
            <div style='min-width:130px;font-weight:800;color:#1A3A8C'>{ds}</div>
            <div style='color:#444;font-size:.93rem'>{txt}</div>
        </div>""", unsafe_allow_html=True)



    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Ulangi dari Awal", type="secondary"):
        for key in ["results", "bench_done", "config"]:
            st.session_state.pop(key, None)
        st.session_state.page = "🏠 Home"; st.rerun()