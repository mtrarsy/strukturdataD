class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, value):
        # Jika tree kosong
        if root is None:
            return Node(value)

        # Masuk ke kiri
        if value < root.value:
            root.left = self.insert(root.left, value)

        # Masuk ke kanan
        else:
            root.right = self.insert(root.right, value)

        return root

    # Implementasi Preorder (Root, Left, Right)
    def preorder(self, root):
        if root:
            print(root.value, end=" ")
            self.preorder(root.left)
            self.preorder(root.right)

    # Implementasi Inorder (Left, Root, Right)
    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.value, end=" ")
            self.inorder(root.right)

    # Implementasi Postorder (Left, Right, Root)
    def postorder(self, root):
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.value, end=" ")

# --- PROGRAM UTAMA ---

# Membuat BST
tree = BST()

# Data awal
data = [50, 30, 70, 20, 40, 60, 80]

# Insert data awal
for item in data:
    tree.root = tree.insert(tree.root, item)

# ==========================================
# JAWABAN NOMOR 1: Tampilkan hasil traversal awal
# ==========================================
print("--- HASIL TRAVERSAL AWAL ---")
print("1. Preorder :")
tree.preorder(tree.root)
print("\n2. Inorder  :")
tree.inorder(tree.root)
print("\n3. Postorder:")
tree.postorder(tree.root)
print("\n")

# ==========================================
# JAWABAN NOMOR 2: Tambahkan node baru
# ==========================================
new_nodes = [10, 90, 65]
print(f"--- Menambahkan Node Baru: {new_nodes} ---")

for item in new_nodes:
    tree.root = tree.insert(tree.root, item)

# ==========================================
# JAWABAN NOMOR 3: Tampilkan hasil setelah penambahan
# ==========================================
print("--- HASIL TRAVERSAL SETELAH PENAMBAHAN ---")
print("a. Preorder :")
tree.preorder(tree.root)
print("\nb. Inorder  :")
tree.inorder(tree.root)
print("\nc. Postorder:")
tree.postorder(tree.root)
print("\n")