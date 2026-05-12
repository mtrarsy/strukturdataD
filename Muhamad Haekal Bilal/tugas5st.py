import streamlit as st

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

    def preorder(self, root, hasil):
        if root:
            hasil.append(str(root.value))
            self.preorder(root.left, hasil)
            self.preorder(root.right, hasil)

    def inorder(self, root, hasil):
        if root:
            self.inorder(root.left, hasil)
            hasil.append(str(root.value))
            self.inorder(root.right, hasil)

    def postorder(self, root, hasil):
        if root:
            self.postorder(root.left, hasil)
            self.postorder(root.right, hasil)
            hasil.append(str(root.value))


st.title("Penyelesaian Tugas Binary Search Tree")
st.write("Implementasi traversal Preorder, Inorder, Postorder dan analisis penambahan node.")
st.divider()

tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
for item in data_awal:
    tree.root = tree.insert(tree.root, item)

st.write("### 1. Hasil Traversal Awal")
pre_awal, in_awal, post_awal = [], [], []
tree.preorder(tree.root, pre_awal)
tree.inorder(tree.root, in_awal)
tree.postorder(tree.root, post_awal)

st.text(f"Preorder  : {' '.join(pre_awal)}")
st.text(f"Inorder   : {' '.join(in_awal)}")
st.text(f"Postorder : {' '.join(post_awal)}")


st.write("### 2 & 3. Hasil Setelah Penambahan Node Baru (10, 90, 65)")
data_baru = [10, 90, 65]
for item in data_baru:
    tree.root = tree.insert(tree.root, item)

pre_baru, in_baru, post_baru = [], [], []
tree.preorder(tree.root, pre_baru)
tree.inorder(tree.root, in_baru)
tree.postorder(tree.root, post_baru)

st.text(f"Preorder  : {' '.join(pre_baru)}")
st.text(f"Inorder   : {' '.join(in_baru)}")
st.text(f"Postorder : {' '.join(post_baru)}")


st.write("### 4. Analisis Perubahan Hasil Traversal")
st.markdown("""
Berdasarkan penambahan data baru, berikut adalah analisis perubahannya:
- *Inorder:* Konsisten menampilkan data secara terurut (ascending) dari nilai terkecil hingga terbesar.
- *Preorder:* Node baru diposisikan sesuai hierarki penelusuran Root-Left-Right, di mana node 10 menjadi anak kiri dari node 20.
- *Postorder:* Node-node baru yang merupakan leaf (daun) akan muncul lebih awal dalam urutan cetak sebelum induknya masing-masing dikunjungi.
""")


st.write("### 5. Visualisasi Struktur Tree (Representasi Teks)")
st.code("""
               50
             /    \\
           30      70
          /  \\    /  \\
        20   40  60   80
       /          \\     \\
     10           65    90
""", language="text")