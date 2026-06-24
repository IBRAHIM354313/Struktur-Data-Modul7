import streamlit as st

# ==============================================================================
# KONFIGURASI HALAMAN UTAMA (Wajib di paling atas & hanya boleh satu kali)
# ==============================================================================
st.set_page_config(page_title="Aplikasi Multi Studi Kasus Stack", page_icon="💻")


# ==============================================================================
# STRUKTUR DATA CLASS (Diletakkan di luar agar tidak ter-reset saat ganti menu)
# ==============================================================================
class StackBuku:
    def __init__(self):
        self.buku = []

    def tambah_buku(self, judul):
        self.buku.append(judul)

    def ambil_buku(self):
        if not self.kosong():
            return self.buku.pop()
        return None

    def lihat_buku_teratas(self):
        if not self.kosong():
            return self.buku[-1]
        return None

    def jumlah_buku(self):
        return len(self.buku)

    def kosong(self):
        return len(self.buku) == 0


class BrowserHistory:
    def __init__(self):
        self.history = []
        self.halaman_sekarang = None

    def kunjungi(self, url):
        if self.halaman_sekarang:
            self.history.append(self.halaman_sekarang)
        self.halaman_sekarang = url

    def back(self):
        if self.history:
            self.halaman_sekarang = self.history.pop()


def cek_validasi_kurung(ekspresi):
    stack = []
    pasangan = {')': '(', ']': '[', '}': '{'}
    for karakter in ekspresi:
        if karakter in pasangan.values():
            stack.append(karakter)
        elif karakter in pasangan.keys():
            if not stack or stack[-1] != pasangan[karakter]:
                return "Tidak Valid"
            stack.pop()
    return "Valid" if not stack else "Tidak Valid"


# ==============================================================================
# MEMBUAT SIDEBAR / MENU PILIHAN DI SEBELAH KIRI
# ==============================================================================
st.sidebar.title("Pilih Studi Kasus")
pilihan = st.sidebar.selectbox(
    "Silakan Pilih:",
    [
        "Tumpukan Buku Perpustakaan", 
        "Browser History", 
        "Undo Editor Teks",
        "Validasi Tanda Kurung",
        "Riwayat Transaksi ATM"
    ]
)


# ==============================================================================
# LOGIKA MENAMPILKAN HALAMAN BERDASARKAN PILIHAN SIDEBAR
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. TUMPUKAN BUKU PERPUSTAKAAN
# ------------------------------------------------------------------------------
if pilihan == "Tumpukan Buku Perpustakaan":
    st.title("📚 Sistem Tumpukan Buku Perpustakaan")

    if "perpustakaan" not in st.session_state:
        st.session_state.perpustakaan = StackBuku()

    perpustakaan = st.session_state.perpustakaan

    st.subheader("Tambah Buku")
    judul = st.text_input("Masukkan Judul Buku")

    if st.button("Tambah Buku"):
        if judul:
            perpustakaan.tambah_buku(judul)
            st.success(f"Buku '{judul}' berhasil ditambahkan")
        else:
            st.warning("Masukkan judul buku terlebih dahulu")

    if st.button("Ambil Buku"):
        buku = perpustakaan.ambil_buku()
        if buku:
            st.success(f"Buku '{buku}' berhasil diambil")
        else:
            st.warning("Tumpukan buku kosong")

    if st.button("Lihat Buku Teratas"):
        buku = perpustakaan.lihat_buku_teratas()
        if buku:
            st.info(f"Buku teratas: {buku}")
        else:
            st.warning("Tidak ada buku dalam tumpukan")

    st.subheader("Informasi Tumpukan")
    st.write(f"Jumlah Buku: **{perpustakaan.jumlah_buku()}**")

    st.subheader("Tumpukan Buku")
    if perpustakaan.kosong():
        st.info("Tumpukan buku kosong")
    else:
        for buku in reversed(perpustakaan.buku):
            st.write(f"📖 {buku}")


# ------------------------------------------------------------------------------
# 2. BROWSER HISTORY
# ------------------------------------------------------------------------------
elif pilihan == "Browser History":
    st.title("🌐 Browser History dengan Fitur Back")

    if "browser" not in st.session_state:
        st.session_state.browser = BrowserHistory()

    browser = st.session_state.browser

    url = st.text_input("Masukkan URL:")

    if st.button("Kunjungi"):
        if url:
            browser.kunjungi(url)

    if st.button("Back"):
        browser.back()

    st.subheader("Halaman Aktif")
    st.write(browser.halaman_sekarang)

    st.subheader("Riwayat")
    if browser.history:
        for item in reversed(browser.history):
            st.write(f"- {item}")
    else:
        st.write("Riwayat kosong")


# ------------------------------------------------------------------------------
# 3. UNDO EDITOR TEKS
# ------------------------------------------------------------------------------
elif pilihan == "Undo Editor Teks":
    st.title("📝 Undo Editor Teks")

    if "history" not in st.session_state:
        st.session_state.history = []

    if "current_text" not in st.session_state:
        st.session_state.current_text = ""

    new_text = st.text_area(
        "Tulis atau edit dokumen:",
        value=st.session_state.current_text,
        height=200
    )

    if st.button("💾 Simpan Perubahan"):
        st.session_state.history.append(new_text)
        st.session_state.current_text = new_text
        st.success("Perubahan berhasil disimpan!")

    if st.button("↩ Undo"):
        if len(st.session_state.history) > 1:
            st.session_state.history.pop()
            st.session_state.current_text = st.session_state.history[-1]
            st.rerun()
        elif len(st.session_state.history) == 1:
            st.session_state.history.pop()
            st.session_state.current_text = ""
            st.rerun()
        else:
            st.warning("Tidak ada perubahan yang bisa di-undo.")

    st.subheader("Dokumen Saat Ini")
    st.text_area("", value=st.session_state.current_text, height=200, disabled=True)

    st.subheader("Riwayat Perubahan")
    if len(st.session_state.history) == 0:
        st.info("Belum ada riwayat perubahan.")
    else:
        for i, version in enumerate(reversed(st.session_state.history), start=1):
            nomor_versi = len(st.session_state.history) - i + 1
            with st.expander(f"Versi {nomor_versi}"):
                st.write(version)


# ------------------------------------------------------------------------------
# 4. VALIDASI TANDA KURUNG
# ------------------------------------------------------------------------------
elif pilihan == "Validasi Tanda Kurung":
    st.title("🔍 Validasi Kurung pada Ekspresi")
    st.write("Masukkan ekspresi matematika yang mengandung tanda kurung (), [], atau {} untuk memeriksa apakah susunannya valid.")

    ekspresi = st.text_input("Masukkan Ekspresi", placeholder="{[a + b] * (c - d)}")

    if st.button("Periksa"):
        if ekspresi.strip() == "":
            st.warning("Silakan masukkan ekspresi terlebih dahulu.")
        else:
            hasil = cek_validasi_kurung(ekspresi)
            if hasil == "Valid":
                st.success(f"Hasil: {hasil} ✅")
            else:
                st.error(f"Hasil: {hasil} ❌")

    st.markdown("---")
    st.subheader("Contoh Input")
    st.code("{[a + b] * (c - d)}\n[a + (b * c)\n([a + b]*c)")


# ------------------------------------------------------------------------------
# 5. RIWAYAT TRANSAKSI ATM
# ------------------------------------------------------------------------------
elif pilihan == "Riwayat Transaksi ATM":
    st.title("🏧 Riwayat Transaksi ATM")

    if "transaksi" not in st.session_state:
        st.session_state.transaksi = []

    transaksi = st.text_input("Masukkan Transaksi")

    if st.button("Tambah Transaksi"):
        if transaksi:
            st.session_state.transaksi.append(transaksi)
            st.success("Transaksi berhasil ditambahkan")

    if st.button("Batalkan Transaksi Terakhir"):
        if st.session_state.transaksi:
            batal = st.session_state.transaksi.pop()
            st.warning(f"Transaksi dibatalkan: {batal}")
        else:
            st.warning("Tidak ada transaksi")

    st.subheader("Riwayat Transaksi")
    if st.session_state.transaksi:
        for t in st.session_state.transaksi:
            st.write(t)
        st.info(f"Transaksi terakhir: {st.session_state.transaksi[-1]}")
    else:
        st.info("Belum ada transaksi")