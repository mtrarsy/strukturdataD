# =========================
# CLASS NODE
# =========================
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# =========================
# CLASS BST
# =========================
class BST:
    def __init__(self):
        self.root = None

    # Insert node
    def insert(self, root, value):

        if root is None:
            return Node(value)

        if value < root.value:
            root.left = self.insert(root.left, value)

        else:
            root.right = self.insert(root.right, value)

        return root

    # Preorder
    def preorder(self, root):
        if root:
            print(root.value, end=" ")
            self.preorder(root.left)
            self.preorder(root.right)

    # Inorder
    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.value, end=" ")
            self.inorder(root.right)

    # Postorder
    def postorder(self, root):
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.value, end=" ")


# =========================
# MEMBUAT BST
# =========================
tree = BST()

data = [50, 30, 70, 20, 40, 60, 80]

for item in data:
    tree.root = tree.insert(tree.root, item)

# =========================
# MENAMBAHKAN NODE BARU
# =========================
tree.root = tree.insert(tree.root, 10)
tree.root = tree.insert(tree.root, 90)
tree.root = tree.insert(tree.root, 65)

# =========================
# HASIL TRAVERSAL
# =========================
print("=== Traversal Setelah Penambahan Node ===")

print("\nPreorder :")
tree.preorder(tree.root)

print("\n\nInorder :")
tree.inorder(tree.root)

print("\n\nPostorder :")
tree.postorder(tree.root)

# =========================
# VISUALISASI TREE
# =========================
print("\n\n=== Struktur BST ===")

print("""
                50
              /    \\
            30      70
           /  \\    /  \\
         20   40  60   80
        /            \\    \\
      10             65    90
""")

# =========================
# ANALISIS
# =========================
print("=== Analisis ===")
print("1. Node 10 masuk ke kiri dari 20 karena lebih kecil.")
print("2. Node 90 masuk ke kanan dari 80 karena lebih besar.")
print("3. Node 65 berada di kanan 60 dan kiri 70.")
print("4. Traversal berubah setelah penambahan node baru.")