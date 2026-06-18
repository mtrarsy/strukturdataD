"""
Implementasi Hash Table — Struktur Data
Informatika UINSSC | MMXXVI

Mencakup:
  - Hash Table dengan Chaining (Separate Chaining)
  - Hash Table dengan Linear Probing (Open Addressing)
  - Demo interaktif di terminal
"""


# ─────────────────────────────────────────────────────────────────────────────
# 1. Hash Table dengan Chaining
# ─────────────────────────────────────────────────────────────────────────────

class Node:
    """Node untuk linked list dalam chaining."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTableChaining:
    """
    Hash Table menggunakan Separate Chaining untuk menangani collision.
    Setiap slot menyimpan linked list dari pasangan (key, value).
    """

    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def _hash(self, key):
        """Fungsi hash: jumlah ASCII karakter (string) atau nilai langsung (int) mod size."""
        if isinstance(key, str):
            return sum(ord(c) for c in key) % self.size
        return int(key) % self.size

    def insert(self, key, value):
        """Menyisipkan pasangan key-value ke dalam tabel."""
        index = self._hash(key)
        new_node = Node(key, value)

        if self.table[index] is None:
            self.table[index] = new_node
        else:
            # Cek apakah key sudah ada → update
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            # Tambah di depan linked list (prepend)
            new_node.next = self.table[index]
            self.table[index] = new_node

        self.count += 1

    def search(self, key):
        """Mencari value berdasarkan key. Mengembalikan value atau None."""
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        """Menghapus key dari tabel. Mengembalikan True jika berhasil."""
        index = self._hash(key)
        current = self.table[index]
        prev = None

        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.count -= 1
                return True
            prev = current
            current = current.next
        return False

    def display(self):
        """Menampilkan isi tabel hash ke terminal."""
        print(f"\n{'─'*50}")
        print(f"  Hash Table (Chaining) — Size: {self.size}, Items: {self.count}")
        print(f"{'─'*50}")
        for i in range(self.size):
            chain = []
            current = self.table[i]
            while current:
                chain.append(f"({current.key}: {current.value})")
                current = current.next
            chain_str = " → ".join(chain) if chain else "[ kosong ]"
            print(f"  [{i:2d}]  {chain_str}")
        print(f"{'─'*50}\n")

    def load_factor(self):
        """Menghitung load factor (rasio isi terhadap kapasitas)."""
        return self.count / self.size


# ─────────────────────────────────────────────────────────────────────────────
# 2. Hash Table dengan Linear Probing
# ─────────────────────────────────────────────────────────────────────────────

DELETED = "__DELETED__"  # Sentinel untuk slot yang dihapus


class HashTableLinearProbing:
    """
    Hash Table menggunakan Open Addressing dengan Linear Probing.
    Jika terjadi collision, cari slot kosong berikutnya secara berurutan.
    """

    def __init__(self, size=10):
        self.size = size
        self.keys = [None] * self.size
        self.values = [None] * self.size
        self.count = 0

    def _hash(self, key):
        if isinstance(key, str):
            return sum(ord(c) for c in key) % self.size
        return int(key) % self.size

    def insert(self, key, value):
        """Menyisipkan key-value. Menggunakan linear probing jika collision."""
        if self.count >= self.size:
            raise Exception("Hash table penuh!")

        index = self._hash(key)
        probe = 0

        while probe < self.size:
            i = (index + probe) % self.size
            if self.keys[i] is None or self.keys[i] == DELETED:
                self.keys[i] = key
                self.values[i] = value
                self.count += 1
                return i  # Kembalikan indeks penyimpanan
            elif self.keys[i] == key:
                self.values[i] = value  # Update nilai
                return i
            probe += 1

        raise Exception("Tabel penuh, tidak bisa menyisipkan.")

    def search(self, key):
        """Mencari value berdasarkan key menggunakan linear probing."""
        index = self._hash(key)
        probe = 0

        while probe < self.size:
            i = (index + probe) % self.size
            if self.keys[i] is None:
                return None  # Slot kosong → key tidak ada
            if self.keys[i] == key:
                return self.values[i]
            probe += 1

        return None

    def delete(self, key):
        """Menghapus key dan menandai slot sebagai DELETED."""
        index = self._hash(key)
        probe = 0

        while probe < self.size:
            i = (index + probe) % self.size
            if self.keys[i] is None:
                return False
            if self.keys[i] == key:
                self.keys[i] = DELETED
                self.values[i] = None
                self.count -= 1
                return True
            probe += 1

        return False

    def display(self):
        """Menampilkan isi tabel hash ke terminal."""
        print(f"\n{'─'*50}")
        print(f"  Hash Table (Linear Probing) — Size: {self.size}, Items: {self.count}")
        print(f"{'─'*50}")
        for i in range(self.size):
            k = self.keys[i]
            v = self.values[i]
            if k is None:
                print(f"  [{i:2d}]  [ kosong ]")
            elif k == DELETED:
                print(f"  [{i:2d}]  [ dihapus ]")
            else:
                print(f"  [{i:2d}]  {k}: {v}")
        print(f"{'─'*50}\n")

    def load_factor(self):
        return self.count / self.size


# ─────────────────────────────────────────────────────────────────────────────
# 3. Demo & Test
# ─────────────────────────────────────────────────────────────────────────────

def demo_chaining():
    print("=" * 55)
    print("  DEMO: Hash Table dengan Chaining")
    print("=" * 55)

    ht = HashTableChaining(size=7)

    # Contoh dari slide: string "ab", "cd", "efg"
    print("\n  Menyisipkan string keys (a=1, b=2, dst.):")
    print('  hash("ab") = (1+2) mod 7 =', (1+2) % 7, '→ indeks 3')
    print('  hash("cd") = (3+4) mod 7 =', (3+4) % 7, '→ indeks 0')
    print('  hash("efg") = (5+6+7) mod 7 =', (5+6+7) % 7, '→ indeks 4')

    ht.insert("cd", "nilai_cd")
    ht.insert("ab", "nilai_ab")
    ht.insert("efg", "nilai_efg")

    # Tambah data integer yang menyebabkan collision
    print("\n  Menyisipkan integer: 14, 5, 9, 1, 24, 21, 77")
    data = [14, 5, 9, 1, 24, 21, 77]
    for d in data:
        ht.insert(d, f"val_{d}")

    ht.display()

    # Test pencarian
    print("  Pencarian:")
    for k in ["ab", "cd", 77, 999]:
        result = ht.search(k)
        status = f"✓ ditemukan → {result}" if result else "✗ tidak ditemukan"
        print(f"    search({k!r:10}) {status}")

    # Test hapus
    print("\n  Hapus key 'ab':", ht.delete("ab"))
    print("  Cari 'ab' setelah dihapus:", ht.search("ab"))
    print(f"\n  Load factor: {ht.load_factor():.2f}")


def demo_linear_probing():
    print("\n" + "=" * 55)
    print("  DEMO: Hash Table dengan Linear Probing")
    print("=" * 55)

    ht = HashTableLinearProbing(size=10)

    # Contoh dari slide: 2001, 13, 11456, 157
    print("\n  Menyisipkan: 2001, 13, 11456, 157, 207")
    data_items = [
        (2001, "data_2001"),
        (13, "data_13"),
        (11456, "data_11456"),
        (157, "data_157"),
    ]

    for key, val in data_items:
        idx = ht.insert(key, val)
        print(f"    insert({key:5d}) → hash={key % 10}, simpan di indeks {idx}")

    print(f"\n  Sisipkan 207 → hash = 207 % 10 = 7")
    print(f"  Indeks 7 sudah ditempati 157 → LINEAR PROBING → cari indeks 8")
    idx = ht.insert(207, "data_207")
    print(f"  207 disimpan di indeks {idx} ✓")

    ht.display()

    # Test pencarian
    print("  Pencarian:")
    for k in [157, 207, 999]:
        result = ht.search(k)
        status = f"✓ ditemukan → {result}" if result else "✗ tidak ditemukan"
        print(f"    search({k}) {status}")

    # Test hapus
    print("\n  Hapus key 157:", ht.delete(157))
    ht.display()
    print(f"  Load factor: {ht.load_factor():.2f}")


def demo_mahasiswa():
    """Simulasi nyata: tabel hash untuk data mahasiswa."""
    print("\n" + "=" * 55)
    print("  DEMO APLIKASI: Data Mahasiswa (NIM → Nama)")
    print("=" * 55)

    ht = HashTableChaining(size=13)

    mahasiswa = [
        ("623C0001", "Ahmad Fauzi"),
        ("623C0002", "Siti Rahmah"),
        ("623C0003", "Budi Santoso"),
        ("623C0004", "Dewi Lestari"),
        ("623C0005", "Rizky Pratama"),
    ]

    print("\n  Menyisipkan data mahasiswa:")
    for nim, nama in mahasiswa:
        ht.insert(nim, nama)
        h = sum(ord(c) for c in nim) % 13
        print(f"    hash({nim}) = {h} → {nama}")

    ht.display()

    print("  Pencarian mahasiswa:")
    for nim in ["623C0004", "623C0099"]:
        result = ht.search(nim)
        if result:
            print(f"    NIM {nim} → {result} ✓")
        else:
            print(f"    NIM {nim} → tidak ditemukan ✗")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo_chaining()
    demo_linear_probing()
    demo_mahasiswa()