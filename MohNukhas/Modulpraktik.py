import streamlit as st
import matplotlib.pyplot as plt

# [cite: 3-7] Definisi struktur Node
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# [cite: 8-10] Definisi struktur kelas BST
class BST:
    def __init__(self):
        self.root = None

    # [cite: 11-21] Fungsi insert untuk memasukkan data sesuai aturan BST
    def insert(self, root, value):
        if root is None:
            return Node(value)
        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)
        return root

    # [cite: 28-32] Traversal Preorder
    def preorder(self, root, res):
        if root:
            res.append(str(root.value))
            self.preorder(root.left, res)
            self.preorder(root.right, res)
        return res

    # [cite: 34-38] Traversal Inorder
    def inorder(self, root, res):
        if root:
            self.inorder(root.left, res)
            res.append(str(root.value))
            self.inorder(root.right, res)
        return res

    # [cite: 40-44] Traversal Postorder
    def postorder(self, root, res):
        if root:
            self.postorder(root.left, res)
            self.postorder(root.right, res)
            res.append(str(root.value))
        return res

    # Fungsi pembantu untuk plot Matplotlib
    def plot_tree(self, node, x, y, dx, ax):
        if node:
            # Gambar lingkaran node
            ax.add_patch(plt.Circle((x, y), 0.5, color='#4CAF50', ec='black', zorder=3))
            ax.text(x, y, str(node.value), ha='center', va='center', fontweight='bold', zorder=4)

            # Gambar garis ke anak kiri
            if node.left:
                ax.plot([x, x - dx], [y - 0.5, y - 2], color='black', lw=1.5, zorder=2)
                self.plot_tree(node.left, x - dx, y - 2, dx / 2, ax)
            
            # Gambar garis ke anak kanan
            if node.right:
                ax.plot([x, x + dx], [y - 0.5, y - 2], color='black', lw=1.5, zorder=2)
                self.plot_tree(node.right, x + dx, y - 2, dx / 2, ax)

# --- APLIKASI STREAMLIT ---
st.title("BST Visualization with Matplotlib")

# Setup Data [cite: 24, 48-50]
data_awal = [50, 30, 70, 20, 40, 60, 80]
data_tambahan = [10, 90, 65]

tree = BST()
# Memasukkan data awal [cite: 25-26]
for item in data_awal + data_tambahan:
    tree.root = tree.insert(tree.root, item)

# Visualisasi Plot
st.subheader("Visualisasi Struktur Tree")
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_aspect('equal')
ax.axis('off')

if tree.root:
    # Parameter: root, x, y, horizontal_spacing, axis
    tree.plot_tree(tree.root, 0, 0, 8, ax)
    # Atur batas tampilan secara otomatis
    ax.relim()
    ax.autoscale_view()

st.pyplot(fig)

# [cite: 51-54] Tampilkan Hasil Traversal
st.divider()
st.subheader("Hasil Traversal")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("**Preorder** [cite: 52]")
    st.code(" ".join(tree.preorder(tree.root, [])))

with c2:
    st.markdown("**Inorder** [cite: 53]")
    st.code(" ".join(tree.inorder(tree.root, [])))

with c3:
    st.markdown("**Postorder** [cite: 54]")
    st.code(" ".join(tree.postorder(tree.root, [])))

# [cite: 55] Analisis Perubahan
st.divider()
st.subheader("Analisis Perubahan")
st.info("""
* **Node 10**: Berada di posisi paling kiri bawah karena nilainya paling kecil ($10 < 20 < 30 < 50$). [cite: 48]
* **Node 90**: Berada di posisi paling kanan bawah karena nilainya paling besar ($90 > 80 > 70 > 50$). [cite: 49]
* **Node 65**: Menempati posisi anak kanan dari node 60 ($60 < 65 < 70$). [cite: 50]
* **Traversal Inorder**: Meskipun ditambahkan secara acak, traversal Inorder tetap menghasilkan urutan angka yang rapi dari terkecil ke terbesar. [cite: 34-38]
""")