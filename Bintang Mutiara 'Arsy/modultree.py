import streamlit as st
import graphviz

# --- DEFENISI STRUKTUR DATA [cite: 3-21] ---
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

    # Metode Helper untuk Traversal [cite: 28-44]
    def get_traversal(self, root, mode):
        res = []
        def preorder(r):
            if r:
                res.append(r.value)
                preorder(r.left)
                preorder(r.right)
        def inorder(r):
            if r:
                inorder(r.left)
                res.append(r.value)
                inorder(r.right)
        def postorder(r):
            if r:
                postorder(r.left)
                postorder(r.right)
                res.append(r.value)
        
        if mode == "pre": preorder(root)
        elif mode == "in": inorder(root)
        else: postorder(root)
        return res

    def visualize(self, root, dot=None):
        if dot is None:
            dot = graphviz.Digraph()
            dot.attr('node', shape='circle', style='filled', fillcolor='lightblue')
            dot.node(str(root.value))
        if root.left:
            dot.edge(str(root.value), str(root.left.value), label="L")
            self.visualize(root.left, dot)
        if root.right:
            dot.edge(str(root.value), str(root.right.value), label="R")
            self.visualize(root.right, dot)
        return dot

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Analisis BST", layout="wide")
st.title("📊 Analisis & Visualisasi Binary Search Tree")

# Inisialisasi Data Awal dan Data Baru [cite: 24, 48-50]
data_awal = [50, 30, 70, 20, 40, 60, 80]
data_tambahan = [10, 90, 65]

# 1. Bangun Tree Awal
tree_awal = BST()
for x in data_awal: tree_awal.root = tree_awal.insert(tree_awal.root, x)

# 2. Bangun Tree Akhir
tree_akhir = BST()
for x in data_awal + data_tambahan: tree_akhir.root = tree_akhir.insert(tree_akhir.root, x)

tab1, tab2 = st.tabs(["Visualisasi", "Analisis Perubahan"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Struktur Awal")
        st.graphviz_chart(tree_awal.visualize(tree_awal.root))
    with col_b:
        st.subheader("Struktur Setelah Penambahan")
        st.graphviz_chart(tree_akhir.visualize(tree_akhir.root))

with tab2:
    st.subheader("🧐 Analisis Hasil Traversal [cite: 55]")
    
    # Hitung Traversal
    in_awal = tree_awal.get_traversal(tree_awal.root, "in")
    in_akhir = tree_akhir.get_traversal(tree_akhir.root, "in")
    
    pre_awal = tree_awal.get_traversal(tree_awal.root, "pre")
    pre_akhir = tree_akhir.get_traversal(tree_akhir.root, "pre")

    # Tampilkan Analisis dalam bentuk Markdown
    st.write(f"""
    **1. Inorder Traversal (Urutan Data):**
    * **Awal:** `{in_awal}`
    * **Setelah Tambah (10, 90, 65):** `{in_akhir}`
    * **Analisis:** Node baru otomatis tersisip sesuai urutan numerik. Nilai **10** menjadi yang terkecil di ujung kiri, dan **90** menjadi yang terbesar di ujung kanan.
    
    **2. Preorder Traversal (Struktur Parent):**
    * **Awal:** `{pre_awal}`
    * **Setelah Tambah:** `{pre_akhir}`
    * **Analisis:** Terlihat adanya penambahan 'daun' baru. Node **10** kini menyambung di bawah node **20**, node **65** di bawah **60**, dan **90** di bawah **80**.
    
    **3. Kesimpulan Properti BST:**
    Meskipun jumlah node bertambah, properti utama BST (kiri < root < kanan) tetap terjaga, yang dibuktikan dengan hasil **Inorder** yang tetap terurut secara *ascending*.
    """)

    st.success("Analisis selesai: Tree berhasil diperbarui tanpa merusak struktur Binary Search Tree.")