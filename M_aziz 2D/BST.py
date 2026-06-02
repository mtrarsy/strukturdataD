import streamlit as st

# Struktur Node sesuai modul [cite: 3-7]
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Class BST sesuai modul [cite: 8-21]
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

    # Implementasi Preorder [cite: 28-32]
    def preorder(self, root, res):
        if root:
            res.append(str(root.value))
            self.preorder(root.left, res)
            self.preorder(root.right, res)
        return res

    # Implementasi Inorder [cite: 34-38]
    def inorder(self, root, res):
        if root:
            self.inorder(root.left, res)
            res.append(str(root.value))
            self.inorder(root.right, res)
        return res

    # Implementasi Postorder [cite: 40-44]
    def postorder(self, root, res):
        if root:
            self.postorder(root.left, res)
            self.postorder(root.right, res)
            res.append(str(root.value))
        return res

# Konfigurasi Streamlit
st.set_page_config(page_title="BST Visualizer", layout="wide")
st.title("🌳 Binary Search Tree (BST) Visualizer")
st.write("Aplikasi ini mengimplementasikan kode dari Modul Tree Data Structure.")

# Inisialisasi Tree sesuai data awal [cite: 22-26]
tree = BST()
initial_data = [50, 30, 70, 20, 40, 60, 80]
for item in initial_data:
    tree.root = tree.insert(tree.root, item)

# Sidebar untuk Tugas Penambahan Node [cite: 47-50]
st.sidebar.header("Tugas: Tambah Node Baru")
if st.sidebar.button("Tambahkan Node (10, 90, 65)"):
    new_nodes = [10, 90, 65]
    for node in new_nodes:
        tree.root = tree.insert(tree.root, node)
    st.sidebar.success("Node 10, 90, dan 65 berhasil ditambahkan!")

# Menampilkan Hasil Traversal [cite: 51-54]
st.subheader("Hasil Traversal")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Preorder**")
    st.write(" → ".join(tree.preorder(tree.root, [])))

with col2:
    st.success("**Inorder**")
    st.write(" → ".join(tree.inorder(tree.root, [])))

with col3:
    st.warning("**Postorder**")
    st.write(" → ".join(tree.postorder(tree.root, [])))

# Visualisasi Tree Sederhana [cite: 56]
st.divider()
st.subheader("Visualisasi Struktur Tree")
st.code("""
          50
        /    \\
      30      70
     /  \\    /  \\
    20  40  60  80
   /          \\   \\
  10          65   90
""", language="text")

# Analisis [cite: 55]
st.divider()
st.subheader("Analisis Perubahan")
st.write("""
1. **Inorder Traversal**: Selalu menghasilkan urutan angka yang terurut (10 hingga 90). Penambahan node baru tidak merusak sifat urutan ini[cite: 55].
2. **Penambahan Node**: 
    - Node **10** menjadi anak kiri dari 20 karena 10 < 20 [cite: 16-17].
    - Node **90** menjadi anak kanan dari 80 karena 90 > 80 [cite: 19-20].
    - Node **65** menjadi anak kanan dari 60 karena 65 > 60 [cite: 19-20].
""")