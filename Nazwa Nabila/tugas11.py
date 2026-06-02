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

# Membuat BST
tree = BST()

# Data awal
data = [50, 30, 70, 20, 40, 60, 80]

print("=== TRAVERSAL SEBELUM PENAMBAHAN NODE BARU ===")
print("Data awal:", data)

for item in data:
    tree.root = tree.insert(tree.root, item)

print("\n1. PREORDER:")
tree.preorder(tree.root)
print("\n")

print("2. INORDER:")
tree.inorder(tree.root)
print("\n")

print("3. POSTORDER:")
tree.postorder(tree.root)
print("\n")

# Tambahkan node baru
print("=== MENAMBAHKAN NODE BARU: 10, 90, 65 ===")
new_nodes = [10, 90, 65]

for item in new_nodes:
    tree.root = tree.insert(tree.root, item)
    print(f"Menambahkan {item}")

print("\n=== TRAVERSAL SETELAH PENAMBAHAN NODE BARU ===")
print("\n1. PREORDER:")
tree.preorder(tree.root)
print("\n")

print("2. INORDER:")
tree.inorder(tree.root)
print("\n")

print("3. POSTORDER:")
tree.postorder(tree.root)
print("\n")