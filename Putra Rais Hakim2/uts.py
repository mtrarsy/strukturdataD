from collections import deque

antrian = deque ()

def daftar(nama) :
     antrian.append(nama)
     print (f"{nama} masuk antrian")

def layani () :
    if antrian:
        print (f"{antrian.popleft () } sedang layani")
    else:
        print("antrian kosong")

daftar("dokumen 1")
daftar("dokumen 2")
layani()
layani()
layani()