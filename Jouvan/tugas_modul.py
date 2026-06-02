import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

# --- LOGIKA BST (Sesuai Struktur Tugas Kamu) ---
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

# --- FUNGSI VISUALISASI UPGRADE ---
def draw_styled_tree(root, new_nodes=[]):
    graph = nx.DiGraph()
    pos = {}
    colors = []
    
    def add_edges(node, x=0, y=0, layer=1):
        if node:
            graph.add_node(node.value)
            pos[node.value] = (x, y)
            
            # Warna beda untuk node baru agar analisis visual lebih gampang
            if node.value in new_nodes:
                colors.append("#FF5722") # Oranye untuk node baru
            else:
                colors.append("#1E88E5") # Biru untuk node lama
            
            if node.left:
                graph.add_edge(node.value, node.left.value)
                add_edges(node.left, x - 1 / 1.5**layer, y - 1, layer + 1)
            if node.right:
                graph.add_edge(node.value, node.right.value)
                add_edges(node.right, x + 1 / 1.5**layer, y - 1, layer + 1)

    add_edges(root)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Gambar garis (edges)
    nx.draw_networkx_edges(graph, pos, width=2, edge_color="#BDBDBD", arrows=True, arrowsize=20)
    
    # Gambar bulatannya (nodes)
    nx.draw_networkx_nodes(graph, pos, node_size=3000, node_color=colors, alpha=0.9)
    
    # Gambar label angka
    nx.draw_networkx_labels(graph, pos, font_size=12, font_color="white", font_weight="bold")
    
    plt.axis("off")
    return fig

# --- UI STREAMLIT ---
st.set_page_config(page_title="BST Analysis Pro", layout="wide")
st.title("🌲 BST Traversal & Visualization")

# Data Setup
tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
for d in data_awal:
    tree.root = tree.insert(tree.root, d)

# Side-by-side Traversal Comparison
st.header("📋 Hasil Traversal")
c1, c2 = st.columns(2)

with c1:
    st.subheader("Kondisi Awal")
    st.info(f"Nodes: {data_awal}")
    st.write("**Preorder:**", " → ".join(map(str, tree.get_traversal(tree.root, "preorder"))))
    st.write("**Inorder:**", " → ".join(map(str, tree.get_traversal(tree.root, "inorder"))))
    st.write("**Postorder:**", " → ".join(map(str, tree.get_traversal(tree.root, "postorder"))))

# Tambah node sesuai tugas
node_baru = [10, 90, 65]
for n in node_baru:
    tree.root = tree.insert(tree.root, n)

with c2:
    st.subheader("Setelah Penambahan")
    st.warning(f"Added: {node_baru}")
    st.write("**Preorder:**", " → ".join(map(str, tree.get_traversal(tree.root, "preorder"))))
    st.write("**Inorder:**", " → ".join(map(str, tree.get_traversal(tree.root, "inorder"))))
    st.write("**Postorder:**", " → ".join(map(str, tree.get_traversal(tree.root, "postorder"))))

st.divider()

# Visualisasi dan Analisis
st.header("🔍 Visualisasi Struktur & Analisis")
col_vis, col_ana = st.columns([2, 1])

with col_vis:
    st.pyplot(draw_styled_tree(tree.root, node_baru))
    st.caption("🔵 Node Awal | 🟠 Node Baru (10, 90, 65)")

with col_ana:
    st.markdown("""
    ### Analisis Perubahan
    
    1. **Stabilitas Inorder**
       Meskipun ada 3 node baru, traversal **Inorder** tetap urut dari 10 ke 90. Ini membuktikan fungsi `insert` menjaga aturan BST.
       
    2. **Posisi Hirarki**
       - **10**: Menjadi *left child* dari 20 karena paling kecil.
       - **90**: Menjadi *right child* dari 80 karena paling besar.
       - **65**: Menjadi *right child* dari 60 karena $60 < 65 < 70$.
       
    3. **Dampak Traversal**
       Node baru selalu muncul di posisi yang lebih dalam (leaf), sehingga pada **Postorder**, node-node ini muncul lebih awal dibanding pendahulunya.
    """)