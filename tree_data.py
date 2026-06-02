import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import time

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BST Visualizer",
    page_icon="🌳",
    layout="wide",
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}

/* Title */
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: #58a6ff !important;
    letter-spacing: -1px;
}

h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #79c0ff !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 12px;
}

/* Traversal result boxes */
.traversal-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 8px 0;
    font-family: 'Fira Code', monospace;
    font-size: 15px;
}

.traversal-box .label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #8b949e;
    margin-bottom: 6px;
}

.traversal-box.preorder  { border-left: 4px solid #f78166; }
.traversal-box.inorder   { border-left: 4px solid #3fb950; }
.traversal-box.postorder { border-left: 4px solid #d2a8ff; }

.traversal-box .values   { color: #e6edf3; font-weight: 600; }

/* Step highlight */
.step-highlight {
    display: inline-block;
    background: #1f2d3d;
    border: 1px solid #58a6ff;
    border-radius: 6px;
    padding: 2px 10px;
    color: #58a6ff;
    font-family: 'Fira Code', monospace;
    margin: 2px;
    font-size: 14px;
}

/* Buttons */
.stButton > button {
    background: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 8px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #30363d;
    border-color: #58a6ff;
    color: #58a6ff;
}

/* Code block */
code {
    background: #161b22 !important;
    color: #79c0ff !important;
    font-family: 'Fira Code', monospace !important;
}

/* Divider */
hr { border-color: #30363d; }

/* Input */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #161b22 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    font-family: 'Fira Code', monospace !important;
}

/* Tab active */
.stTabs [aria-selected="true"] {
    color: #58a6ff !important;
    border-bottom-color: #58a6ff !important;
}
</style>
""", unsafe_allow_html=True)


# ─── BST IMPLEMENTATION ────────────────────────────────────────────────────────
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
        elif value > root.value:
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

    def search(self, root, value):
        if root is None or root.value == value:
            return root
        if value < root.value:
            return self.search(root.left, value)
        return self.search(root.right, value)

    def height(self, root):
        if root is None:
            return 0
        return 1 + max(self.height(root.left), self.height(root.right))

    def count_nodes(self, root):
        if root is None:
            return 0
        return 1 + self.count_nodes(root.left) + self.count_nodes(root.right)


# ─── GRAPH BUILDER ─────────────────────────────────────────────────────────────
def build_graph(node, graph, pos, x=0, y=0, level=1, x_offset=None):
    if node is None:
        return
    if x_offset is None:
        x_offset = 2.0

    graph.add_node(node.value)
    pos[node.value] = (x, y)

    gap = x_offset / (2 ** (level - 1))

    if node.left:
        graph.add_edge(node.value, node.left.value)
        build_graph(node.left, graph, pos, x - gap, y - 1.5, level + 1, x_offset)
    if node.right:
        graph.add_edge(node.value, node.right.value)
        build_graph(node.right, graph, pos, x + gap, y - 1.5, level + 1, x_offset)


def draw_bst(tree, highlight_nodes=None, highlight_color=None, title="Binary Search Tree"):
    if tree.root is None:
        fig, ax = plt.subplots(figsize=(8, 3))
        fig.patch.set_facecolor("#0d1117")
        ax.set_facecolor("#0d1117")
        ax.text(0.5, 0.5, "Tree kosong — tambahkan node dulu",
                ha='center', va='center', color='#8b949e', fontsize=13,
                fontfamily='monospace')
        ax.axis('off')
        return fig

    G = nx.DiGraph()
    pos = {}
    build_graph(tree.root, G, pos)

    highlight_nodes = highlight_nodes or []
    if highlight_color is None:
        highlight_color = {}

    node_colors = []
    node_sizes  = []
    node_edge_colors = []

    for node in G.nodes():
        if node in highlight_color:
            node_colors.append(highlight_color[node])
            node_sizes.append(1400)
            node_edge_colors.append("#ffffff")
        elif node in highlight_nodes:
            node_colors.append("#f78166")
            node_sizes.append(1400)
            node_edge_colors.append("#ffffff")
        else:
            node_colors.append("#1f2d3d")
            node_sizes.append(1100)
            node_edge_colors.append("#58a6ff")

    fig, ax = plt.subplots(figsize=(max(10, len(G.nodes()) * 1.2), 6))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")

    nx.draw_networkx_edges(G, pos, ax=ax,
                           edge_color="#30363d",
                           arrows=True,
                           arrowstyle="-|>",
                           arrowsize=18,
                           width=2,
                           connectionstyle="arc3,rad=0.0")

    nx.draw_networkx_nodes(G, pos, ax=ax,
                           node_color=node_colors,
                           node_size=node_sizes,
                           edgecolors=node_edge_colors,
                           linewidths=2)

    nx.draw_networkx_labels(G, pos, ax=ax,
                            font_color="#e6edf3",
                            font_size=13,
                            font_weight="bold",
                            font_family="monospace")

    ax.set_title(title, color="#58a6ff", fontsize=15,
                 fontweight="bold", pad=15, fontfamily="monospace")
    ax.axis("off")
    plt.tight_layout()
    return fig


# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "tree" not in st.session_state:
    st.session_state.tree = BST()
    default_data = [50, 30, 70, 20, 40, 60, 80]
    for v in default_data:
        st.session_state.tree.root = st.session_state.tree.insert(
            st.session_state.tree.root, v)

tree: BST = st.session_state.tree


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌳 BST Visualizer")
    st.markdown("---")

    st.markdown("### ➕ Insert Node")
    new_val = st.number_input("Nilai baru", min_value=-9999, max_value=9999,
                               value=0, step=1, key="insert_val")
    if st.button("Insert", use_container_width=True):
        if tree.search(tree.root, new_val):
            st.warning(f"Nilai {new_val} sudah ada di tree!")
        else:
            tree.root = tree.insert(tree.root, new_val)
            st.success(f"✅ {new_val} berhasil ditambahkan")
            st.rerun()

    st.markdown("---")
    st.markdown("### 🔍 Search Node")
    search_val = st.number_input("Nilai dicari", min_value=-9999, max_value=9999,
                                  value=0, step=1, key="search_val")
    if st.button("Search", use_container_width=True):
        found = tree.search(tree.root, search_val)
        if found:
            st.success(f"✅ Node {search_val} ditemukan!")
            st.session_state["searched"] = search_val
        else:
            st.error(f"❌ Node {search_val} tidak ditemukan")
            st.session_state["searched"] = None

    st.markdown("---")
    st.markdown("### 🗑️ Reset Tree")
    if st.button("Reset ke Default", use_container_width=True):
        st.session_state.tree = BST()
        default_data = [50, 30, 70, 20, 40, 60, 80]
        for v in default_data:
            st.session_state.tree.root = st.session_state.tree.insert(
                st.session_state.tree.root, v)
        st.session_state.pop("searched", None)
        st.rerun()

    if st.button("Bersihkan Tree", use_container_width=True):
        st.session_state.tree = BST()
        st.session_state.pop("searched", None)
        st.rerun()

    st.markdown("---")
    st.markdown("### 📥 Input Custom Data")
    custom_input = st.text_input("Masukkan angka (pisah koma)", placeholder="10,25,5,40")
    if st.button("Build Tree", use_container_width=True):
        try:
            values = [int(x.strip()) for x in custom_input.split(",") if x.strip()]
            if values:
                st.session_state.tree = BST()
                for v in values:
                    st.session_state.tree.root = st.session_state.tree.insert(
                        st.session_state.tree.root, v)
                st.session_state.pop("searched", None)
                st.success(f"✅ Tree dibuat dari {len(values)} nilai")
                st.rerun()
        except ValueError:
            st.error("Format salah! Gunakan angka dipisah koma.")


# ─── MAIN CONTENT ──────────────────────────────────────────────────────────────
st.title("🌳 Binary Search Tree Visualizer")
st.markdown("Visualisasi interaktif BST dengan traversal **Preorder**, **Inorder**, dan **Postorder**")

# Metrics
col1, col2, col3, col4 = st.columns(4)
node_count = tree.count_nodes(tree.root)
tree_height = tree.height(tree.root)

with col1:
    st.metric("Total Node", node_count)
with col2:
    st.metric("Tinggi Tree", tree_height)
with col3:
    root_val = tree.root.value if tree.root else "–"
    st.metric("Root", root_val)
with col4:
    inorder_vals = tree.inorder(tree.root)
    min_val = min(inorder_vals) if inorder_vals else "–"
    max_val = max(inorder_vals) if inorder_vals else "–"
    st.metric("Min / Max", f"{min_val} / {max_val}")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌲 Tree View", "🔄 Traversal", "🎬 Animasi Step", "📖 Penjelasan"])

# ── TAB 1: Tree View ──────────────────────────────────────────────────────────
with tab1:
    searched = st.session_state.get("searched", None)
    if searched is not None:
        highlight_color = {searched: "#f78166"}
        fig = draw_bst(tree, highlight_color=highlight_color,
                       title=f"BST — Node {searched} ditandai 🔴")
    else:
        fig = draw_bst(tree, title="Binary Search Tree")
    st.pyplot(fig)
    plt.close()

# ── TAB 2: Traversal ─────────────────────────────────────────────────────────
with tab2:
    pre  = tree.preorder(tree.root)
    ino  = tree.inorder(tree.root)
    post = tree.postorder(tree.root)

    def fmt(vals):
        return " → ".join(str(v) for v in vals) if vals else "(kosong)"

    st.markdown(f"""
    <div class="traversal-box preorder">
        <div class="label">🔴 Preorder &nbsp;|&nbsp; Root → Left → Right</div>
        <div class="values">{fmt(pre)}</div>
    </div>
    <div class="traversal-box inorder">
        <div class="label">🟢 Inorder &nbsp;&nbsp;|&nbsp; Left → Root → Right &nbsp;(Sorted ✓)</div>
        <div class="values">{fmt(ino)}</div>
    </div>
    <div class="traversal-box postorder">
        <div class="label">🟣 Postorder |&nbsp; Left → Right → Root</div>
        <div class="values">{fmt(post)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Perbandingan Visual")

    col_a, col_b, col_c = st.columns(3)

    def mini_traversal_fig(vals, color, label):
        fig, ax = plt.subplots(figsize=(5, 1.4))
        fig.patch.set_facecolor("#161b22")
        ax.set_facecolor("#161b22")
        for i, v in enumerate(vals):
            ax.add_patch(mpatches.FancyBboxPatch((i * 1.1, 0.1), 0.9, 0.8,
                boxstyle="round,pad=0.05", facecolor=color, alpha=0.85,
                edgecolor="#0d1117", linewidth=1.5))
            ax.text(i * 1.1 + 0.45, 0.5, str(v), ha='center', va='center',
                    color='white', fontsize=11, fontweight='bold',
                    fontfamily='monospace')
        ax.set_xlim(-0.1, len(vals) * 1.1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title(label, color=color, fontsize=11, fontweight='bold',
                     fontfamily='monospace')
        plt.tight_layout()
        return fig

    if pre:
        with col_a:
            f1 = mini_traversal_fig(pre, "#f78166", "Preorder")
            st.pyplot(f1); plt.close()
        with col_b:
            f2 = mini_traversal_fig(ino, "#3fb950", "Inorder")
            st.pyplot(f2); plt.close()
        with col_c:
            f3 = mini_traversal_fig(post, "#d2a8ff", "Postorder")
            st.pyplot(f3); plt.close()

# ── TAB 3: Animasi Step ───────────────────────────────────────────────────────
with tab3:
    st.markdown("#### 🎬 Traversal Step-by-Step")
    traversal_type = st.selectbox("Pilih jenis traversal:",
                                   ["Preorder", "Inorder", "Postorder"])
    speed = st.slider("Kecepatan (detik per step)", 0.1, 1.5, 0.5, 0.1)

    if st.button("▶ Jalankan Animasi", use_container_width=True):
        if tree.root is None:
            st.warning("Tree kosong!")
        else:
            if traversal_type == "Preorder":
                steps = tree.preorder(tree.root)
                color = "#f78166"
            elif traversal_type == "Inorder":
                steps = tree.inorder(tree.root)
                color = "#3fb950"
            else:
                steps = tree.postorder(tree.root)
                color = "#d2a8ff"

            visited = []
            tree_placeholder = st.empty()
            info_placeholder = st.empty()
            progress_bar = st.progress(0)

            for i, node_val in enumerate(steps):
                visited.append(node_val)
                hc = {v: color for v in visited}
                hc[node_val] = "#ffd700"  # current node gold

                fig = draw_bst(tree, highlight_color=hc,
                               title=f"{traversal_type} — Step {i+1}/{len(steps)}: mengunjungi node {node_val}")
                tree_placeholder.pyplot(fig)
                plt.close()

                visited_str = " → ".join(
                    f'<span class="step-highlight">{v}</span>' for v in visited)
                info_placeholder.markdown(
                    f"<div style='margin-top:8px'>Dikunjungi: {visited_str}</div>",
                    unsafe_allow_html=True)

                progress_bar.progress((i + 1) / len(steps))
                time.sleep(speed)

            info_placeholder.markdown(
                f"<div style='margin-top:8px; color:#3fb950; font-weight:600'>"
                f"✅ {traversal_type} selesai! Urutan: "
                + " → ".join(f'<span class="step-highlight">{v}</span>' for v in visited)
                + "</div>",
                unsafe_allow_html=True)

# ── TAB 4: Penjelasan ─────────────────────────────────────────────────────────
with tab4:
    st.markdown("""
    ### Apa itu Binary Search Tree?

    **BST** adalah struktur data pohon di mana setiap node memiliki aturan:
    - Node **kiri** < Node saat ini
    - Node **kanan** > Node saat ini

    ---

    ### Jenis-Jenis Traversal

    | Traversal | Urutan Kunjungan | Kegunaan |
    |-----------|-----------------|----------|
    | **Preorder** | Root → Kiri → Kanan | Menyalin / serialize tree |
    | **Inorder** | Kiri → Root → Kanan | Menghasilkan data **terurut** |
    | **Postorder** | Kiri → Kanan → Root | Menghapus tree, evaluasi ekspresi |

    ---

    ### Contoh Kode Python
    """)

    st.code("""
class BST:
    def preorder(self, root, result=[]):
        if root:
            result.append(root.value)   # Root dulu
            self.preorder(root.left)    # Lalu kiri
            self.preorder(root.right)   # Lalu kanan
        return result

    def inorder(self, root, result=[]):
        if root:
            self.inorder(root.left)     # Kiri dulu
            result.append(root.value)   # Lalu root
            self.inorder(root.right)    # Lalu kanan
        return result

    def postorder(self, root, result=[]):
        if root:
            self.postorder(root.left)   # Kiri dulu
            self.postorder(root.right)  # Lalu kanan
            result.append(root.value)   # Root terakhir
        return result
    """, language="python")

    st.markdown("""
    ---
    ### Kompleksitas Waktu

    | Operasi | Average Case | Worst Case |
    |---------|-------------|------------|
    | Insert  | O(log n)    | O(n)       |
    | Search  | O(log n)    | O(n)       |
    | Traversal | O(n)     | O(n)       |
    """)