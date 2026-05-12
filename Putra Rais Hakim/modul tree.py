import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import io

# ─────────────────────────────────────────
# BST Implementation
# ─────────────────────────────────────────

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, value):
        if root is None:
            return Node(value)
        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)
        return root

    def preorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            result.append(root.value)
            self.preorder(root.left, result)
            self.preorder(root.right, result)
        return result

    def inorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.inorder(root.left, result)
            result.append(root.value)
            self.inorder(root.right, result)
        return result

    def postorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.value)
        return result

# ─────────────────────────────────────────
# Build tree helpers
# ─────────────────────────────────────────

def build_tree(data):
    tree = BST()
    for item in data:
        tree.root = tree.insert(tree.root, item)
    return tree

BASE_DATA = [50, 30, 70, 20, 40, 60, 80]

def get_tree_stages():
    stages = {}

    # Stage 0: BST awal
    stages["awal"] = build_tree(BASE_DATA)

    # Stage 1: Tambah 10
    stages["tambah_10"] = build_tree(BASE_DATA + [10])

    # Stage 2: Tambah 10, 90
    stages["tambah_90"] = build_tree(BASE_DATA + [10, 90])

    # Stage 3: Tambah 10, 90, 65
    stages["tambah_65"] = build_tree(BASE_DATA + [10, 90, 65])

    return stages

# ─────────────────────────────────────────
# Tree Drawing
# ─────────────────────────────────────────

def compute_positions(node, x=0, y=0, x_offset=2.5, positions=None, parent=None, edges=None):
    if positions is None:
        positions = {}
    if edges is None:
        edges = []

    if node is None:
        return positions, edges

    positions[node.value] = (x, y)

    if parent is not None:
        edges.append((parent, node.value))

    compute_positions(node.left,  x - x_offset, y - 1.8, x_offset / 1.8, positions, node.value, edges)
    compute_positions(node.right, x + x_offset, y - 1.8, x_offset / 1.8, positions, node.value, edges)

    return positions, edges


def draw_tree(tree, title="BST", highlight_nodes=None, figsize=(8, 5)):
    if highlight_nodes is None:
        highlight_nodes = set()

    positions, edges = compute_positions(tree.root)

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")
    ax.axis("off")

    # Draw edges
    for parent, child in edges:
        x1, y1 = positions[parent]
        x2, y2 = positions[child]
        ax.plot([x1, x2], [y1, y2], color="#334155", linewidth=1.8, zorder=1)

    # Draw nodes
    for val, (x, y) in positions.items():
        is_new = val in highlight_nodes
        circle_color = "#f59e0b" if is_new else "#1e40af"
        border_color = "#fbbf24" if is_new else "#3b82f6"

        circle = plt.Circle((x, y), 0.45, color=circle_color, zorder=2)
        ax.add_patch(circle)
        circle_border = plt.Circle((x, y), 0.45, fill=False, edgecolor=border_color, linewidth=2, zorder=3)
        ax.add_patch(circle_border)
        ax.text(x, y, str(val), ha="center", va="center",
                fontsize=11, fontweight="bold",
                color="white", zorder=4)

    # Legend
    if highlight_nodes:
        new_patch = mpatches.Patch(color="#f59e0b", label="Node Baru")
        old_patch = mpatches.Patch(color="#1e40af", label="Node Lama")
        ax.legend(handles=[old_patch, new_patch], loc="upper right",
                  facecolor="#1e293b", labelcolor="white", fontsize=9, framealpha=0.9)

    ax.set_title(title, color="#e2e8f0", fontsize=13, fontweight="bold", pad=12)

    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    ax.set_xlim(min(xs) - 1.2, max(xs) + 1.2)
    ax.set_ylim(min(ys) - 1.2, max(ys) + 1.2)

    plt.tight_layout()
    return fig

# ─────────────────────────────────────────
# Streamlit UI
# ─────────────────────────────────────────

st.set_page_config(
    page_title="BST Visualizer",
    page_icon="🌳",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Sora:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
        background-color: #0f172a;
        color: #e2e8f0;
    }
    .stApp { background-color: #0f172a; }

    h1, h2, h3 { color: #f1f5f9 !important; }

    .traversal-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
        font-family: 'JetBrains Mono', monospace;
    }
    .traversal-label {
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .traversal-values {
        font-size: 15px;
        color: #38bdf8;
        font-weight: 700;
    }
    .highlight-new { color: #fbbf24; font-weight: bold; }
    .section-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 24px;
    }
    .badge {
        display: inline-block;
        background: #1d4ed8;
        color: white;
        border-radius: 999px;
        padding: 2px 12px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .analysis-box {
        background: #0f2744;
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 8px 0;
        font-size: 14px;
        color: #cbd5e1;
    }
    code {
        background: #0f172a;
        color: #34d399;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ───
st.markdown("# 🌳 BST — Binary Search Tree Visualizer")
st.markdown("**Modul Tree Data Structure** · Implementasi & Analisis Traversal")
st.markdown("---")

stages = get_tree_stages()

# ═══════════════════════════════════════════════
# BAGIAN 1 — Traversal BST Awal
# ═══════════════════════════════════════════════
st.markdown("## 📌 Bagian 1 — Traversal BST Awal")
st.markdown(f"Data awal: `{BASE_DATA}`")

tree_awal = stages["awal"]
pre  = tree_awal.preorder(tree_awal.root)
ino  = tree_awal.inorder(tree_awal.root)
post = tree_awal.postorder(tree_awal.root)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">TRAVERSAL</span>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="traversal-box">
        <div class="traversal-label">Preorder (Root → Left → Right)</div>
        <div class="traversal-values">{" → ".join(map(str, pre))}</div>
    </div>
    <div class="traversal-box">
        <div class="traversal-label">Inorder (Left → Root → Right)</div>
        <div class="traversal-values">{" → ".join(map(str, ino))}</div>
    </div>
    <div class="traversal-box">
        <div class="traversal-label">Postorder (Left → Right → Root)</div>
        <div class="traversal-values">{" → ".join(map(str, post))}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    fig = draw_tree(tree_awal, title="BST Awal", figsize=(7, 4.5))
    st.pyplot(fig)
    plt.close()

# ═══════════════════════════════════════════════
# BAGIAN 2a — Tambah Node 10
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown("## ➕ Bagian 2a — Tambahkan Node `10`")

tree_10 = stages["tambah_10"]
pre_10  = tree_10.preorder(tree_10.root)
ino_10  = tree_10.inorder(tree_10.root)
post_10 = tree_10.postorder(tree_10.root)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">SETELAH TAMBAH 10</span>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="traversal-box">
        <div class="traversal-label">Preorder</div>
        <div class="traversal-values">{" → ".join(
            [f'<span class="highlight-new">{v}</span>' if v == 10 else str(v) for v in pre_10]
        )}</div>
    </div>
    <div class="traversal-box">
        <div class="traversal-label">Inorder</div>
        <div class="traversal-values">{" → ".join(
            [f'<span class="highlight-new">{v}</span>' if v == 10 else str(v) for v in ino_10]
        )}</div>
    </div>
    <div class="traversal-box">
        <div class="traversal-label">Postorder</div>
        <div class="traversal-values">{" → ".join(
            [f'<span class="highlight-new">{v}</span>' if v == 10 else str(v) for v in post_10]
        )}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="analysis-box">
        📊 <b>Analisis:</b> Node <code>10</code> masuk ke kiri <code>20</code> (10 &lt; 50 &lt; 30 &lt; 20).
        Inorder tetap terurut — posisi <code>10</code> muncul di awal karena nilai terkecil.
        Preorder & Postorder merefleksikan posisi di sub-pohon kiri bawah.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    fig = draw_tree(tree_10, title="BST setelah tambah node 10", highlight_nodes={10}, figsize=(7, 5))
    st.pyplot(fig)
    plt.close()

# ═══════════════════════════════════════════════
# BAGIAN 2b — Tambah Node 90
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown("## ➕ Bagian 2b — Tambahkan Node `90`")

tree_90 = stages["tambah_90"]
pre_90  = tree_90.preorder(tree_90.root)
ino_90  = tree_90.inorder(tree_90.root)
post_90 = tree_90.postorder(tree_90.root)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">SETELAH TAMBAH 10, 90</span>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="traversal-box">
        <div class="traversal-label">Preorder</div>
        <div class="traversal-values">{" → ".join(
            [f'<span class="highlight-new">{v}</span>' if v == 90 else str(v) for v in pre_90]
        )}</div>
    </div>
    <div class="traversal-box">
        <div class="traversal-label">Inorder</div>
        <div class="traversal-values">{" → ".join(
            [f'<span class="highlight-new">{v}</span>' if v == 90 else str(v) for v in ino_90]
        )}</div>
    </div>
    <div class="traversal-box">
        <div class="traversal-label">Postorder</div>
        <div class="traversal-values">{" → ".join(
            [f'<span class="highlight-new">{v}</span>' if v == 90 else str(v) for v in post_90]
        )}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="analysis-box">
        📊 <b>Analisis:</b> Node <code>90</code> masuk ke kanan <code>80</code> (90 &gt; 50 &gt; 70 &gt; 80).
        Inorder tetap terurut — <code>90</code> muncul di akhir karena nilai terbesar.
        Postorder menempatkan <code>90</code> sebelum <code>80</code>, lalu naik ke atas.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    fig = draw_tree(tree_90, title="BST setelah tambah node 10 & 90", highlight_nodes={90}, figsize=(7, 5.5))
    st.pyplot(fig)
    plt.close()

# ═══════════════════════════════════════════════
# BAGIAN 2c — Tambah Node 65
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown("## ➕ Bagian 2c — Tambahkan Node `65`")

tree_65 = stages["tambah_65"]
pre_65  = tree_65.preorder(tree_65.root)
ino_65  = tree_65.inorder(tree_65.root)
post_65 = tree_65.postorder(tree_65.root)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge">SETELAH TAMBAH 10, 90, 65</span>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="traversal-box">
        <div class="traversal-label">Preorder</div>
        <div class="traversal-values">{" → ".join(
            [f'<span class="highlight-new">{v}</span>' if v == 65 else str(v) for v in pre_65]
        )}</div>
    </div>
    <div class="traversal-box">
        <div class="traversal-label">Inorder</div>
        <div class="traversal-values">{" → ".join(
            [f'<span class="highlight-new">{v}</span>' if v == 65 else str(v) for v in ino_65]
        )}</div>
    </div>
    <div class="traversal-box">
        <div class="traversal-label">Postorder</div>
        <div class="traversal-values">{" → ".join(
            [f'<span class="highlight-new">{v}</span>' if v == 65 else str(v) for v in post_65]
        )}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="analysis-box">
        📊 <b>Analisis:</b> Node <code>65</code> masuk ke kanan <code>60</code> (65 &gt; 50 &gt; 70, lalu 65 &lt; 70 → kiri 70, lalu 65 &gt; 60 → kanan 60).
        Inorder menampilkan <code>65</code> di antara <code>60</code> dan <code>70</code> — urutan tetap terjaga.
        Preorder menunjukkan <code>65</code> langsung setelah <code>60</code>.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    fig = draw_tree(tree_65, title="BST Final (semua node)", highlight_nodes={65}, figsize=(7, 5.5))
    st.pyplot(fig)
    plt.close()

# ═══════════════════════════════════════════════
# RINGKASAN PERBANDINGAN
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown("## 📊 Ringkasan Perbandingan Traversal")

data_awal = BASE_DATA
data_10   = BASE_DATA + [10]
data_90   = BASE_DATA + [10, 90]
data_65   = BASE_DATA + [10, 90, 65]

labels   = ["Awal", "+10", "+90", "+65"]
datasets = [data_awal, data_10, data_90, data_65]
trees    = [stages["awal"], stages["tambah_10"], stages["tambah_90"], stages["tambah_65"]]

rows_pre  = []
rows_ino  = []
rows_post = []

for label, t in zip(labels, trees):
    rows_pre.append( {"Tahap": label, "Traversal": " → ".join(map(str, t.preorder(t.root)))} )
    rows_ino.append( {"Tahap": label, "Traversal": " → ".join(map(str, t.inorder(t.root)))} )
    rows_post.append({"Tahap": label, "Traversal": " → ".join(map(str, t.postorder(t.root)))} )

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Preorder**")
    for r in rows_pre:
        st.markdown(f"""
        <div class="traversal-box" style="padding:10px 14px;margin:4px 0;">
            <div class="traversal-label">{r['Tahap']}</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#38bdf8;">{r['Traversal']}</div>
        </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("**Inorder**")
    for r in rows_ino:
        st.markdown(f"""
        <div class="traversal-box" style="padding:10px 14px;margin:4px 0;">
            <div class="traversal-label">{r['Tahap']}</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#38bdf8;">{r['Traversal']}</div>
        </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("**Postorder**")
    for r in rows_post:
        st.markdown(f"""
        <div class="traversal-box" style="padding:10px 14px;margin:4px 0;">
            <div class="traversal-label">{r['Tahap']}</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#34d399;">{r['Traversal']}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#475569;font-size:13px;padding:12px 0;">
    🌳 BST Visualizer · Modul Tree Data Structure · Dibuat dengan Streamlit
</div>
""", unsafe_allow_html=True)