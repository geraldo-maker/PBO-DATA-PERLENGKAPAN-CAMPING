"""
Aplikasi Peralatan Camping - GUI (Tkinter), satu file.
Jalankan: python app_gui.py
"""
import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont

FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_DATA = os.path.join(FOLDER, "peralatan.csv")
HEADER = ["Kode", "Nama", "Kategori", "Jumlah", "Kondisi"]
OPSI_KONDISI = ["Baik", "Perlu diperiksa", "Rusak"]
SEMUA = "Semua kategori"

DATA_AWAL = [
    ["CAMP001", "Tenda Dome", "Tempat tinggal", 4, "Baik"],
    ["CAMP002", "Sleeping Bag", "Perlengkapan tidur", 8, "Baik"],
    ["CAMP003", "Kompor Portable", "Memasak", 3, "Baik"],
    ["CAMP004", "Lampu Camping", "Penerangan", 6, "Baik"],
    ["CAMP005", "Matras", "Perlengkapan tidur", 10, "Baik"],
    ["CAMP006", "Carrier 50L", "Tas", 5, "Perlu diperiksa"],
    ["CAMP007", "Trekking Pole", "Pendakian", 6, "Baik"],
    ["CAMP008", "Jas Hujan", "Pakaian", 7, "Baik"],
]

WARNA = {
    "bg": "#F4F1EA",
    "panel": "#FFFFFF",
    "hijau": "#2F6B4F",
    "hijau_tua": "#1F4D38",
    "hijau_muda": "#E3EFE8",
    "teks": "#22312B",
    "abu": "#7A877F",
    "garis": "#DDD8CC",
    "zebra": "#FAF8F3",
    "kuning": "#B7791F",
    "merah": "#C0483A",
    "oranye": "#D98E2B",
}


# --------------------------------------------------------------------------
# Model & data
# --------------------------------------------------------------------------
class Peralatan:
    def __init__(self, kode, nama, kategori, jumlah, kondisi):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.jumlah = int(jumlah)
        self.kondisi = kondisi

    def to_list(self):
        return [self.kode, self.nama, self.kategori, self.jumlah, self.kondisi]


class PeralatanRepository:
    """Membaca dan menulis data peralatan ke file CSV."""

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            self.simpan([Peralatan(*baris) for baris in DATA_AWAL])

    def muat(self):
        daftar = []
        with open(self.path, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                daftar.append(Peralatan(
                    row["Kode"], row["Nama"], row["Kategori"],
                    row["Jumlah"], row["Kondisi"],
                ))
        return daftar

    def simpan(self, daftar):
        with open(self.path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)
            for item in daftar:
                writer.writerow(item.to_list())


# --------------------------------------------------------------------------
# Komponen UI
# --------------------------------------------------------------------------
class KartuStatistik(tk.Frame):
    """Kartu ringkasan dengan garis aksen di sisi kiri."""

    def __init__(self, master, caption, warna_aksen, fonts):
        super().__init__(master, bg=WARNA["panel"],
                         highlightbackground=WARNA["garis"], highlightthickness=1)
        tk.Frame(self, bg=warna_aksen, width=6).pack(side="left", fill="y")
        isi = tk.Frame(self, bg=WARNA["panel"])
        isi.pack(side="left", fill="both", expand=True, padx=16, pady=12)
        self.nilai = tk.Label(isi, text="0", font=fonts["angka"],
                              bg=WARNA["panel"], fg=WARNA["teks"], anchor="w")
        self.nilai.pack(fill="x")
        tk.Label(isi, text=caption, font=fonts["kecil"],
                 bg=WARNA["panel"], fg=WARNA["abu"], anchor="w").pack(fill="x")

    def set(self, nilai):
        self.nilai.config(text=str(nilai))


class FormPeralatan(tk.Toplevel):
    """Dialog untuk menambah atau mengubah peralatan."""

    def __init__(self, master, fonts, daftar_kategori, on_simpan, item=None):
        super().__init__(master, bg=WARNA["panel"])
        self.on_simpan = on_simpan
        self.item = item
        self.title("Ubah Peralatan" if item else "Tambah Peralatan")
        self.resizable(False, False)
        self.transient(master)

        header = tk.Frame(self, bg=WARNA["hijau"])
        header.pack(fill="x")
        tk.Label(header, text="Ubah Peralatan" if item else "Tambah Peralatan",
                 font=fonts["judul_kecil"], bg=WARNA["hijau"], fg="white",
                 padx=24, pady=14).pack(anchor="w")

        body = tk.Frame(self, bg=WARNA["panel"], padx=24, pady=18)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)

        self.v_kode = tk.StringVar(value=item.kode if item else "")
        self.v_nama = tk.StringVar(value=item.nama if item else "")
        self.v_kategori = tk.StringVar(value=item.kategori if item else "")
        self.v_jumlah = tk.StringVar(value=str(item.jumlah) if item else "1")
        self.v_kondisi = tk.StringVar(value=item.kondisi if item else "Baik")

        baris = [
            ("Kode", ttk.Entry(body, textvariable=self.v_kode, width=32)),
            ("Nama", ttk.Entry(body, textvariable=self.v_nama, width=32)),
            ("Kategori", ttk.Combobox(body, textvariable=self.v_kategori,
                                      values=daftar_kategori, width=30)),
            ("Jumlah", ttk.Spinbox(body, from_=0, to=9999,
                                   textvariable=self.v_jumlah, width=10)),
            ("Kondisi", ttk.Combobox(body, textvariable=self.v_kondisi,
                                     values=OPSI_KONDISI, state="readonly", width=30)),
        ]
        self.field = {}
        for i, (label, widget) in enumerate(baris):
            tk.Label(body, text=label, font=fonts["label"], bg=WARNA["panel"],
                     fg=WARNA["teks"]).grid(row=i, column=0, sticky="w", pady=7, padx=(0, 16))
            widget.grid(row=i, column=1, sticky="ew", pady=7, ipady=3)
            self.field[label] = widget

        if item:  # kode tidak boleh diubah saat edit
            self.field["Kode"].state(["disabled"])

        self.lbl_error = tk.Label(body, text="", font=fonts["kecil"],
                                  bg=WARNA["panel"], fg=WARNA["merah"],
                                  anchor="w", justify="left", wraplength=320)
        self.lbl_error.grid(row=len(baris), column=0, columnspan=2, sticky="ew", pady=(4, 0))

        tombol = tk.Frame(self, bg=WARNA["panel"], padx=24)
        tombol.pack(fill="x", pady=(0, 20))
        ttk.Button(tombol, text="Simpan", style="Aksen.TButton",
                   command=self._simpan).pack(side="right")
        ttk.Button(tombol, text="Batal", style="Biasa.TButton",
                   command=self.destroy).pack(side="right", padx=(0, 10))

        self.bind("<Return>", lambda e: self._simpan())
        self.bind("<Escape>", lambda e: self.destroy())

        self.update_idletasks()
        x = master.winfo_rootx() + (master.winfo_width() - self.winfo_width()) // 2
        y = master.winfo_rooty() + (master.winfo_height() - self.winfo_height()) // 3
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        self.grab_set()
        (self.field["Nama"] if item else self.field["Kode"]).focus_set()

    def _simpan(self):
        kode = self.v_kode.get().strip().upper()
        nama = self.v_nama.get().strip()
        kategori = self.v_kategori.get().strip()
        jumlah_text = self.v_jumlah.get().strip()
        kondisi = self.v_kondisi.get().strip()

        if not all([kode, nama, kategori, jumlah_text, kondisi]):
            self.lbl_error.config(text="Semua kolom wajib diisi.")
            return
        try:
            jumlah = int(jumlah_text)
        except ValueError:
            self.lbl_error.config(text="Jumlah harus berupa bilangan bulat.")
            return
        if jumlah < 0:
            self.lbl_error.config(text="Jumlah tidak boleh negatif.")
            return

        pesan = self.on_simpan(Peralatan(kode, nama, kategori, jumlah, kondisi),
                               self.item is not None)
        if pesan:
            self.lbl_error.config(text=pesan)
        else:
            self.destroy()


# --------------------------------------------------------------------------
# Jendela utama
# --------------------------------------------------------------------------
class AplikasiCamping(tk.Tk):
    KOLOM = [
        ("kode", "Kode", 110, "w"),
        ("nama", "Nama", 240, "w"),
        ("kategori", "Kategori", 200, "w"),
        ("jumlah", "Jumlah", 90, "center"),
        ("kondisi", "Kondisi", 160, "w"),
    ]

    def __init__(self):
        super().__init__()
        self.title("Peralatan Camping")
        self.geometry("1000x660")
        self.minsize(880, 580)
        self.configure(bg=WARNA["bg"])

        self.repo = PeralatanRepository(FILE_DATA)
        self.daftar = self.repo.muat()
        self.urut_kolom = "kode"
        self.urut_turun = False

        self._siapkan_font()
        self._siapkan_style()
        self._bangun_header()
        self._bangun_kartu()
        self._bangun_toolbar()
        self._bangun_tabel()
        self._bangun_statusbar()
        self.segarkan()

        self.bind("<Control-n>", lambda e: self.tambah())
        self.bind("<Control-f>", lambda e: self.ent_cari.focus_set())
        self.bind("<F5>", lambda e: self.muat_ulang())

    # ---- gaya ------------------------------------------------------------
    def _siapkan_font(self):
        tersedia = set(tkfont.families())
        pilihan = ["Segoe UI", "SF Pro Text", "Helvetica Neue", "Ubuntu", "DejaVu Sans"]
        keluarga = next((f for f in pilihan if f in tersedia), "TkDefaultFont")
        self.fonts = {
            "judul": (keluarga, 20, "bold"),
            "judul_kecil": (keluarga, 14, "bold"),
            "angka": (keluarga, 24, "bold"),
            "label": (keluarga, 10, "bold"),
            "normal": (keluarga, 10),
            "kecil": (keluarga, 9),
        }
        self.keluarga = keluarga
        self.option_add("*TCombobox*Listbox.font", (keluarga, 10))

    def _siapkan_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        f = self.keluarga

        s.configure("TEntry", fieldbackground="white", bordercolor=WARNA["garis"],
                    lightcolor=WARNA["garis"], darkcolor=WARNA["garis"],
                    padding=6, font=(f, 10))
        s.map("TEntry", bordercolor=[("focus", WARNA["hijau"])],
              lightcolor=[("focus", WARNA["hijau"])],
              darkcolor=[("focus", WARNA["hijau"])])
        s.configure("TCombobox", fieldbackground="white", background="white",
                    bordercolor=WARNA["garis"], arrowcolor=WARNA["hijau"],
                    padding=5, font=(f, 10))
        s.map("TCombobox", fieldbackground=[("readonly", "white")],
              bordercolor=[("focus", WARNA["hijau"])])
        s.configure("TSpinbox", fieldbackground="white", bordercolor=WARNA["garis"],
                    padding=5, font=(f, 10))

        s.configure("Aksen.TButton", background=WARNA["hijau"], foreground="white",
                    font=(f, 10, "bold"), padding=(18, 8), borderwidth=0, focusthickness=0)
        s.map("Aksen.TButton",
              background=[("active", WARNA["hijau_tua"]), ("pressed", WARNA["hijau_tua"])])
        s.configure("Biasa.TButton", background="white", foreground=WARNA["teks"],
                    font=(f, 10), padding=(16, 8), bordercolor=WARNA["garis"],
                    borderwidth=1, focusthickness=0)
        s.map("Biasa.TButton", background=[("active", WARNA["hijau_muda"])])
        s.configure("Bahaya.TButton", background="white", foreground=WARNA["merah"],
                    font=(f, 10), padding=(16, 8), bordercolor=WARNA["garis"],
                    borderwidth=1, focusthickness=0)
        s.map("Bahaya.TButton", background=[("active", "#FBE9E6")])

        s.configure("Treeview", background="white", fieldbackground="white",
                    foreground=WARNA["teks"], rowheight=36, borderwidth=0,
                    font=(f, 10))
        s.map("Treeview", background=[("selected", WARNA["hijau_muda"])],
              foreground=[("selected", WARNA["hijau_tua"])])
        s.configure("Treeview.Heading", background=WARNA["hijau_tua"],
                    foreground="white", font=(f, 10, "bold"),
                    padding=(10, 9), borderwidth=0, relief="flat")
        s.map("Treeview.Heading", background=[("active", WARNA["hijau"])])
        s.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        s.configure("Vertical.TScrollbar", background=WARNA["garis"],
                    troughcolor=WARNA["bg"], bordercolor=WARNA["bg"],
                    arrowcolor=WARNA["abu"])

    # ---- tata letak ------------------------------------------------------
    def _bangun_header(self):
        header = tk.Frame(self, bg=WARNA["hijau_tua"])
        header.pack(fill="x")
        isi = tk.Frame(header, bg=WARNA["hijau_tua"])
        isi.pack(fill="x", padx=28, pady=18)

        ikon = tk.Canvas(isi, width=46, height=46, bg=WARNA["hijau_tua"],
                         highlightthickness=0)
        ikon.pack(side="left", padx=(0, 14))
        ikon.create_oval(2, 2, 44, 44, fill=WARNA["hijau"], outline="")
        ikon.create_polygon(23, 11, 38, 34, 8, 34, fill="#F4F1EA", outline="")
        ikon.create_polygon(23, 21, 29, 34, 17, 34, fill=WARNA["hijau_tua"], outline="")
        ikon.create_line(6, 35, 40, 35, fill="#F4F1EA", width=2)

        teks = tk.Frame(isi, bg=WARNA["hijau_tua"])
        teks.pack(side="left")
        tk.Label(teks, text="Peralatan Camping", font=self.fonts["judul"],
                 bg=WARNA["hijau_tua"], fg="white").pack(anchor="w")
        tk.Label(teks, text="Kelola stok dan kondisi perlengkapan dengan mudah",
                 font=self.fonts["normal"], bg=WARNA["hijau_tua"],
                 fg="#B9D4C5").pack(anchor="w")

    def _bangun_kartu(self):
        baris = tk.Frame(self, bg=WARNA["bg"])
        baris.pack(fill="x", padx=28, pady=(20, 4))
        for i in range(3):
            baris.columnconfigure(i, weight=1, uniform="kartu")

        self.kartu_jenis = KartuStatistik(baris, "Jenis peralatan", WARNA["hijau"], self.fonts)
        self.kartu_unit = KartuStatistik(baris, "Total unit", "#4C8FB5", self.fonts)
        self.kartu_cek = KartuStatistik(baris, "Perlu perhatian", WARNA["oranye"], self.fonts)
        for i, kartu in enumerate((self.kartu_jenis, self.kartu_unit, self.kartu_cek)):
            kartu.grid(row=0, column=i, sticky="ew",
                       padx=(0 if i == 0 else 8, 0 if i == 2 else 8))

    def _bangun_toolbar(self):
        bar = tk.Frame(self, bg=WARNA["bg"])
        bar.pack(fill="x", padx=28, pady=(16, 10))

        tk.Label(bar, text="Cari", font=self.fonts["label"], bg=WARNA["bg"],
                 fg=WARNA["teks"]).pack(side="left", padx=(0, 8))
        self.v_cari = tk.StringVar()
        self.v_cari.trace_add("write", lambda *a: self.segarkan())
        self.ent_cari = ttk.Entry(bar, textvariable=self.v_cari, width=28)
        self.ent_cari.pack(side="left", ipady=3)

        self.v_kategori = tk.StringVar(value=SEMUA)
        self.cmb_kategori = ttk.Combobox(bar, textvariable=self.v_kategori,
                                         state="readonly", width=22)
        self.cmb_kategori.pack(side="left", padx=(12, 0), ipady=3)
        self.cmb_kategori.bind("<<ComboboxSelected>>", lambda e: self.segarkan())

        ttk.Button(bar, text="+  Tambah", style="Aksen.TButton",
                   command=self.tambah).pack(side="right")
        ttk.Button(bar, text="Hapus", style="Bahaya.TButton",
                   command=self.hapus).pack(side="right", padx=(0, 8))
        ttk.Button(bar, text="Ubah", style="Biasa.TButton",
                   command=self.ubah).pack(side="right", padx=(0, 8))

    def _bangun_tabel(self):
        bingkai = tk.Frame(self, bg=WARNA["panel"],
                           highlightbackground=WARNA["garis"], highlightthickness=1)
        bingkai.pack(fill="both", expand=True, padx=28, pady=(0, 8))

        self.tree = ttk.Treeview(bingkai, columns=[k[0] for k in self.KOLOM],
                                 show="headings", selectmode="browse")
        for kunci, judul, lebar, rata in self.KOLOM:
            self.tree.heading(kunci, text=judul,
                              anchor=("w" if rata == "w" else "center"),
                              command=lambda k=kunci: self.urutkan(k))
            self.tree.column(kunci, width=lebar, anchor=rata, minwidth=70)
        self.tree.column("nama", stretch=True)

        scroll = ttk.Scrollbar(bingkai, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.tag_configure("ganjil", background=WARNA["zebra"])
        self.tree.tag_configure("perlu", foreground=WARNA["kuning"])
        self.tree.tag_configure("rusak", foreground=WARNA["merah"])
        self.tree.bind("<Double-1>", lambda e: self.ubah())
        self.tree.bind("<Delete>", lambda e: self.hapus())

        self.lbl_kosong = tk.Label(bingkai, text="Tidak ada peralatan yang cocok",
                                   font=self.fonts["normal"], bg="white", fg=WARNA["abu"])

    def _bangun_statusbar(self):
        self.v_status = tk.StringVar()
        tk.Label(self, textvariable=self.v_status, font=self.fonts["kecil"],
                 bg=WARNA["bg"], fg=WARNA["abu"], anchor="w").pack(
            fill="x", padx=30, pady=(0, 10))

    # ---- logika tampilan -------------------------------------------------
    def _terfilter(self):
        kata = self.v_cari.get().strip().lower()
        kategori = self.v_kategori.get()
        hasil = []
        for it in self.daftar:
            if kategori != SEMUA and it.kategori != kategori:
                continue
            if kata and kata not in f"{it.kode} {it.nama} {it.kategori}".lower():
                continue
            hasil.append(it)

        def kunci(it):
            nilai = getattr(it, self.urut_kolom)
            return nilai if isinstance(nilai, int) else str(nilai).lower()

        return sorted(hasil, key=kunci, reverse=self.urut_turun)

    def segarkan(self):
        kategori = sorted({it.kategori for it in self.daftar}, key=str.lower)
        self.cmb_kategori["values"] = [SEMUA] + kategori
        if self.v_kategori.get() not in [SEMUA] + kategori:
            self.v_kategori.set(SEMUA)

        terpilih = self.tree.selection()
        self.tree.delete(*self.tree.get_children())
        tampil = self._terfilter()
        for i, it in enumerate(tampil):
            tags = ["ganjil"] if i % 2 else []
            if it.kondisi == "Perlu diperiksa":
                tags.append("perlu")
            elif it.kondisi == "Rusak":
                tags.append("rusak")
            titik = "●  " if it.kondisi != "Baik" else "○  "
            self.tree.insert("", "end", iid=it.kode, tags=tags,
                             values=(it.kode, it.nama, it.kategori, it.jumlah,
                                     titik + it.kondisi))
        if terpilih and self.tree.exists(terpilih[0]):
            self.tree.selection_set(terpilih[0])

        for kunci, judul, _, _ in self.KOLOM:
            panah = ""
            if kunci == self.urut_kolom:
                panah = "  ▼" if self.urut_turun else "  ▲"
            self.tree.heading(kunci, text=judul + panah)

        self.kartu_jenis.set(len(self.daftar))
        self.kartu_unit.set(sum(it.jumlah for it in self.daftar))
        self.kartu_cek.set(sum(1 for it in self.daftar if it.kondisi != "Baik"))
        self.v_status.set(
            f"Menampilkan {len(tampil)} dari {len(self.daftar)} peralatan   •   "
            "Ctrl+N tambah   •   Ctrl+F cari   •   Klik dua kali untuk mengubah")
        if tampil:
            self.lbl_kosong.place_forget()
        else:
            self.lbl_kosong.place(relx=0.5, rely=0.5, anchor="center")

    def urutkan(self, kolom):
        if self.urut_kolom == kolom:
            self.urut_turun = not self.urut_turun
        else:
            self.urut_kolom, self.urut_turun = kolom, False
        self.segarkan()

    def muat_ulang(self):
        self.daftar = self.repo.muat()
        self.segarkan()

    # ---- aksi ------------------------------------------------------------
    def _item_terpilih(self):
        pilihan = self.tree.selection()
        if not pilihan:
            messagebox.showinfo("Pilih data",
                                "Pilih satu peralatan di tabel terlebih dahulu.",
                                parent=self)
            return None
        return next((it for it in self.daftar if it.kode == pilihan[0]), None)

    def _kategori_ada(self):
        return sorted({it.kategori for it in self.daftar}, key=str.lower)

    def _terima(self, item_baru, mode_ubah):
        if mode_ubah:
            for i, it in enumerate(self.daftar):
                if it.kode == item_baru.kode:
                    self.daftar[i] = item_baru
                    break
        else:
            if any(it.kode == item_baru.kode for it in self.daftar):
                return "Kode tersebut sudah digunakan."
            self.daftar.append(item_baru)
        self.repo.simpan(self.daftar)
        self.segarkan()
        if self.tree.exists(item_baru.kode):
            self.tree.selection_set(item_baru.kode)
            self.tree.see(item_baru.kode)
        return None

    def tambah(self):
        FormPeralatan(self, self.fonts, self._kategori_ada(), self._terima)

    def ubah(self):
        item = self._item_terpilih()
        if item:
            FormPeralatan(self, self.fonts, self._kategori_ada(), self._terima, item)

    def hapus(self):
        if not self.tree.selection():
            return
        item = self._item_terpilih()
        if item and messagebox.askyesno(
                "Hapus peralatan",
                f"Hapus '{item.nama}' ({item.kode}) dari daftar?", parent=self):
            self.daftar.remove(item)
            self.repo.simpan(self.daftar)
            self.segarkan()


if __name__ == "__main__":
    AplikasiCamping().mainloop()