import streamlit as st

# =========================
# JUDUL
# =========================
st.title("Visualisasi BST Setelah Semua Node Dimasukkan")

# =========================
# VISUALISASI BST
# =========================
st.code("""
                50
              /    \\
            30      70
           /  \\    /  \\
         20   40  60   80
        /            \\    \\
      10             65    90
""", language="text")

# =========================
# KETERANGAN
# =========================
st.subheader("Keterangan")

st.write("• Node 10 berada di kiri 20 karena nilainya lebih kecil.")
st.write("• Node 90 berada di kanan 80 karena nilainya lebih besar.")
st.write("• Node 65 berada di kanan 60 dan kiri 70.")
st.write("• Semua node tersusun sesuai aturan Binary Search Tree (BST).")