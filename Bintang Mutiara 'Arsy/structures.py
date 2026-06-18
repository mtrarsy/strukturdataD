# ================================================
#  structures.py
#  Implementasi 4 Struktur Data:
#  Array/List, BST, Hash Table, AVL Tree
# ================================================


# ── 1. ARRAY / LIST ─────────────────────────────
class ArrayDS:
    def __init__(self):
        self.data = []

    def insert(self, value):
        self.data.append(value)

    def search(self, value):
        """Linear Search — O(n)"""
        for i, v in enumerate(self.data):
            if v == value:
                return i
        return -1

    def delete(self, value):
        """O(n)"""
        try:
            self.data.remove(value)
            return True
        except ValueError:
            return False

    def size(self):
        return len(self.data)


# ── 2. BINARY SEARCH TREE (BST) ─────────────────
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left  = None
        self.right = None


class BST:
    def __init__(self):
        self.root  = None
        self._size = 0

    def insert(self, value):
        self.root = self._insert(self.root, value)
        self._size += 1

    def _insert(self, node, value):
        if node is None:
            return BSTNode(value)
        if value < node.value:
            node.left  = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node

    def search(self, value):
        """Binary Search — O(log n) rata-rata"""
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def delete(self, value):
        self.root, deleted = self._delete(self.root, value)
        if deleted:
            self._size -= 1
        return deleted

    def _delete(self, node, value):
        if node is None:
            return node, False
        deleted = False
        if value < node.value:
            node.left,  deleted = self._delete(node.left, value)
        elif value > node.value:
            node.right, deleted = self._delete(node.right, value)
        else:
            deleted = True
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            succ = node.right
            while succ.left:
                succ = succ.left
            node.value = succ.value
            node.right, _ = self._delete(node.right, succ.value)
        return node, deleted

    def size(self):
        return self._size


# ── 3. HASH TABLE ────────────────────────────────
class HashTable:
    def __init__(self, capacity=2048):
        self.capacity = capacity
        self.buckets  = [[] for _ in range(capacity)]
        self._size    = 0

    def _hash(self, value):
        return hash(value) % self.capacity

    def insert(self, value):
        idx = self._hash(value)
        if value not in self.buckets[idx]:
            self.buckets[idx].append(value)
            self._size += 1

    def search(self, value):
        """O(1) rata-rata"""
        return value in self.buckets[self._hash(value)]

    def delete(self, value):
        idx = self._hash(value)
        if value in self.buckets[idx]:
            self.buckets[idx].remove(value)
            self._size -= 1
            return True
        return False

    def size(self):
        return self._size


# ── 4. AVL TREE ──────────────────────────────────
class AVLNode:
    def __init__(self, value):
        self.value  = value
        self.left   = None
        self.right  = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root  = None
        self._size = 0

    def _h(self, n):
        return n.height if n else 0

    def _bf(self, n):
        return self._h(n.left) - self._h(n.right)

    def _upd(self, n):
        n.height = 1 + max(self._h(n.left), self._h(n.right))

    def _rr(self, y):          # rotate right
        x = y.left; T2 = x.right
        x.right = y; y.left = T2
        self._upd(y); self._upd(x)
        return x

    def _rl(self, x):          # rotate left
        y = x.right; T2 = y.left
        y.left = x; x.right = T2
        self._upd(x); self._upd(y)
        return y

    def _balance(self, n):
        self._upd(n)
        bf = self._bf(n)
        if bf > 1:
            if self._bf(n.left) < 0:
                n.left = self._rl(n.left)
            return self._rr(n)
        if bf < -1:
            if self._bf(n.right) > 0:
                n.right = self._rr(n.right)
            return self._rl(n)
        return n

    def insert(self, value):
        self.root = self._insert(self.root, value)
        self._size += 1

    def _insert(self, n, value):
        if n is None:
            return AVLNode(value)
        if value < n.value:
            n.left  = self._insert(n.left, value)
        elif value > n.value:
            n.right = self._insert(n.right, value)
        else:
            return n
        return self._balance(n)

    def search(self, value):
        """O(log n) dijamin"""
        return self._search(self.root, value)

    def _search(self, n, value):
        if n is None:
            return False
        if value == n.value:
            return True
        if value < n.value:
            return self._search(n.left, value)
        return self._search(n.right, value)

    def delete(self, value):
        self.root, deleted = self._delete(self.root, value)
        if deleted:
            self._size -= 1
        return deleted

    def _delete(self, n, value):
        if n is None:
            return n, False
        deleted = False
        if value < n.value:
            n.left,  deleted = self._delete(n.left, value)
        elif value > n.value:
            n.right, deleted = self._delete(n.right, value)
        else:
            deleted = True
            if n.left is None:
                return n.right, deleted
            if n.right is None:
                return n.left, deleted
            succ = n.right
            while succ.left:
                succ = succ.left
            n.value = succ.value
            n.right, _ = self._delete(n.right, succ.value)
        return self._balance(n), deleted

    def size(self):
        return self._size