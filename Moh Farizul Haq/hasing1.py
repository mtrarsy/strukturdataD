class HashTable:
    def __init__(self, size=10):
        self.size = size
        # Membuat array/list kosong sebanyak 'size' untuk chaining
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key):
        # Menggunakan rumus modulus sederhana sebagai fungsi hash
        return key % self.size

    def insert(self, key, value):
        hash_index = self._hash_function(key)
        
        # Cek apakah key sudah ada, jika ada maka update nilainya
        for i, kv in enumerate(self.table[hash_index]):
            if kv[0] == key:
                self.table[hash_index][i] = (key, value)
                print(f"[INFO] Key {key} sudah ada. Nilai diupdate menjadi '{value}'.")
                return
        
        # Jika belum ada, tambahkan data baru ke dalam list (Chaining)
        self.table[hash_index].append((key, value))
        print(f"[SUKSES] Data ({key}: '{value}') berhasil dimasukkan ke Indeks Hash: {hash_index}")

    def search(self, key):
        hash_index = self._hash_function(key)
        for k, v in self.table[hash_index]:
            if k == key:
                return v
        return None

    def display_table(self):
        print("\n=== KONDISI HASH TABLE (CHAINING) ===")
        for idx, bucket in enumerate(self.table):
            if bucket:
                # Menggabungkan isi rantai data (chain) agar rapi saat dicetak
                chain = " -> ".join([f"[{k}: {v}]" for k, v in bucket])
                print(f"Indeks {idx}: {chain}")
            else:
                print(f"Indeks {idx}: [Kosong]")
        print("=====================================\n")

# Fungsi Utama Menu Terminal
def main():
    # Inisialisasi hash table dengan ukuran 10 slot
    hash_table = HashTable(size=10)
    
    # Data awal simulasi agar terminal tidak kosong saat pertama dijalankan
    hash_table.insert(15, "Andi")
    hash_table.insert(25, "Budi") # Ini akan menyebabkan collision di indeks 5 dengan Andi
    hash_table.insert(7, "Cici")

    while True:
        print("\n--- MENU IMPLEMENTASI HASHING ---")
        print("1. Tampilkan Hash Table")
        print("2. Tambah Data (Insert)")
        print("3. Cari Data (Search)")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1/2/3/4): ").strip()
        
        if pilihan == "1":
            hash_table.display_table()
        elif pilihan == "2":
            try:
                key = int(input("Masukkan Key (Angka/ID integer): "))
                value = input("Masukkan Value (Nama/Data teks): ")
                hash_table.insert(key, value)
            except ValueError:
                print("[ERROR] Key harus berupa angka integer!")
        elif pilihan == "3":
            try:
                key = int(input("Masukkan Key yang dicari: "))
                hasil = hash_table.search(key)
                if hasil:
                    print(f"[FOUND] Data ditemukan! Nilai untuk Key {key} adalah '{hasil}'.")
                else:
                    print(f"[NOT FOUND] Data dengan Key {key} tidak ditemukan.")
            except ValueError:
                print("[ERROR] Key harus berupa angka integer!")
        elif pilihan == "4":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("[WARN] Pilihan menu tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()