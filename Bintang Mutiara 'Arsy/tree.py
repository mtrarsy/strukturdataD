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

# Inisialisasi awal
tree = BST()
data_awal = [50, 30, 70, 20, 40, 60, 80]
for item in data_awal:
    tree.root = tree.insert(tree.root, item)

print("--- Hasil Traversal Awal ---")
print("Preorder :", end=" "); tree.preorder(tree.root); print()
print("Inorder  :", end=" "); tree.inorder(tree.root); print()
print("Postorder:", end=" "); tree.postorder(tree.root); print()

# Penambahan node baru: 10, 90, 65
node_baru = [10, 90, 65]
for item in node_baru:
    tree.root = tree.insert(tree.root, item)

print("\n--- Hasil Traversal Setelah Penambahan (10, 90, 65) ---")
print("Preorder :", end=" "); tree.preorder(tree.root); print()
print("Inorder  :", end=" "); tree.inorder(tree.root); print()
print("Postorder:", end=" "); tree.postorder(tree.root); print()