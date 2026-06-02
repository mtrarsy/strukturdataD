class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    # Fungsi insert node
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


# Membuat BST
tree = BST()

data = [50, 30, 70, 20, 40, 60, 80]

for item in data:
    tree.root = tree.insert(tree.root, item)

# Menampilkan hasil traversal
print("Preorder : ")
tree.preorder(tree.root)

print("\nInorder : ")
tree.inorder(tree.root)

print("\nPostorder : ")
tree.postorder(tree.root)