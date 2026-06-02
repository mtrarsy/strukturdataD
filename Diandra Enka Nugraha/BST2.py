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

    def preorder(self, root):
        if root:
            print(root.value, end=" ")
            self.preorder(root.left)
            self.preorder(root.right)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.value, end=" ")
            self.inorder(root.right)

    def postorder(self, root):
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.value, end=" ")


# ============================================================
# MEMBUAT BST — DATA AWAL
# ============================================================
tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]

for item in data_awal:
    tree.root = tree.insert(tree.root, item)

# ============================================================
# TUGAS 1: Traversal SEBELUM penambahan node baru
# ============================================================
print("=" * 50)
print("TRAVERSAL SEBELUM PENAMBAHAN NODE BARU")
print("Data awal:", data_awal)
print("=" * 50)

print("Preorder  : ", end="")
tree.preorder(tree.root)
print()

print("Inorder   : ", end="")
tree.inorder(tree.root)
print()

print("Postorder : ", end="")
tree.postorder(tree.root)
print()

# ============================================================
# TUGAS 2: Tambahkan node baru: 10, 90, 65
# ============================================================
node_baru = [10, 90, 65]
for item in node_baru:
    tree.root = tree.insert(tree.root, item)

# ============================================================
# TUGAS 3: Traversal SETELAH penambahan node baru
# ============================================================
print()
print("=" * 50)
print("TRAVERSAL SETELAH PENAMBAHAN NODE BARU (10, 90, 65)")
print("=" * 50)

print("Preorder  : ", end="")
tree.preorder(tree.root)
print()

print("Inorder   : ", end="")
tree.inorder(tree.root)
print()

print("Postorder : ", end="")
tree.postorder(tree.root)
print()

# ============================================================
# TUGAS 4: Analisis perubahan traversal
# ============================================================
print()
print("=" * 50)
print("ANALISIS PERUBAHAN TRAVERSAL")
print("=" * 50)
print("""
[PREORDER — Root, Left, Right]
  Sebelum: 50 30 20 40 70 60 80
  Sesudah : 50 30 20 10 40 70 60 65 80 90
  Perubahan:
  - Node 10 muncul setelah 20 (anak kiri 20)
  - Node 65 muncul setelah 60 (anak kanan 60)
  - Node 90 muncul setelah 80 (anak kanan 80)

[INORDER — Left, Root, Right]
  Sebelum: 20 30 40 50 60 70 80
  Sesudah : 10 20 30 40 50 60 65 70 80 90
  Perubahan:
  - Inorder selalu menghasilkan urutan TERURUT ASCENDING
  - 10 ditambahkan di depan (nilai terkecil)
  - 65 disisipkan antara 60 dan 70
  - 90 ditambahkan di akhir (nilai terbesar)

[POSTORDER — Left, Right, Root]
  Sebelum: 20 40 30 60 80 70 50
  Sesudah : 10 20 40 30 65 60 90 80 70 50
  Perubahan:
  - Node 10 muncul sebelum 20 (diproses lebih dulu sebagai daun kiri)
  - Node 65 muncul sebelum 60
  - Node 90 muncul sebelum 80

[KESIMPULAN]
  - Inorder BST selalu menghasilkan urutan terurut (sorted)
  - Posisi kemunculan node baru bergantung pada posisinya di tree
  - Node daun (leaf) baru muncul lebih awal di Postorder,
    lebih akhir di Preorder, dan tersisip di Inorder
""")