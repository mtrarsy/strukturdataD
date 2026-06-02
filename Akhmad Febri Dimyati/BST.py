import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

# LOGIKA BST
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

    def get_traversal(self, root, mode="inorder"):
        res = []
        if root:
            if mode == "preorder":
                res.append(root.value)
                res.extend(self.get_traversal(root.left, mode))
                res.extend(self.get_traversal(root.right, mode))
            elif mode == "inorder":
                res.extend(self.get_traversal(root.left, mode))
                res.append(root.value)
                res.extend(self.get_traversal(root.right, mode))
            elif mode == "postorder":
                res.extend(self.get_traversal(root.left, mode))
                res.extend(self.get_traversal(root.right, mode))
                res.append(root.value)
        return res

# FUNGSI VISUALISASI
def draw_tree(root):
    graph = nx.DiGraph()
    pos = {}
    
    def add_edges(node, x=0, y=0, layer=1):
        if node:
            graph.add_node(node.value)
            pos[node.value] = (x, y)
            if node.left:
                graph.add_edge(node.value, node.left.value)
                add_edges(node.left, x - 1 / 2**layer, y - 1, layer + 1)
            if node.right:
                graph.add_edge(node.value, node.right.value)
                add_edges(node.right, x + 1 / 2**layer, y - 1, layer + 1)

    add_edges(root)
    fig, ax = plt.subplots(figsize=(10, 7))
    nx.draw(graph, pos, with_labels=True, node_size=2500, node_color="#4CAF50", 
            font_size=12, font_weight="bold", font_color="white", 
            arrows=True, edge_color="#555", width=2, ax=ax)
    return fig

# UI STREAMLIT
st.set_page_config(page_title="BST Visualizer", layout="wide")
st.title("🌳 Tree Data Structure: BST Implementation")
st.markdown("Dashboard ini menampilkan hasil tugas implementasi Binary Search Tree.")

# Inisialisasi Data
tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
for d in data_awal:
    tree.root = tree.insert(tree.root, d)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Data Awal")
    st.code(f"Input: {data_awal}")
    st.write("**Preorder:**", tree.get_traversal(tree.root, "preorder"))
    st.write("**Inorder:**", tree.get_traversal(tree.root, "inorder"))
    st.write("**Postorder:**", tree.get_traversal(tree.root, "postorder"))

# Tambah Node Baru
node_baru = [10, 90, 65]
for n in node_baru:
    tree.root = tree.insert(tree.root, n)

with col2:
    st.subheader("2. Setelah Penambahan Node")
    st.info(f"Ditambahkan: {node_baru}")
    st.write("**Preorder:**", tree.get_traversal(tree.root, "preorder"))
    st.write("**Inorder:**", tree.get_traversal(tree.root, "inorder"))
    st.write("**Postorder:**", tree.get_traversal(tree.root, "postorder"))

st.divider()

# Analisis & Visualisasi
st.subheader("3. Analisis Perubahan & Visualisasi Final")
tab1, tab2 = st.tabs(["📊 Analisis", "🖼️ Visualisasi Tree"])

with tab1:
    st.markdown("""
    - **Urutan Inorder Tetap Terurut:** Meskipun node 10, 90, dan 65 ditambahkan, hasil traversal Inorder tetap urut ($10, 20, ..., 90$). Ini membuktikan properti BST bekerja dengan benar.
    - **Efek Node Baru:** 
        - Node **10** (paling kecil) menjadi anak paling kiri (sub-tree dari 20).
        - Node **90** (paling besar) menjadi anak paling kanan (sub-tree dari 80).
        - Node **65** menyisip di antara 60 dan 70 sebagai anak kanan dari 60.
    """)

with tab2:
    fig = draw_tree(tree.root)
    st.pyplot(fig)

# Semua jawaban 1 - 5 ada di kode, tinggal jalanin streamlitnya aja pak