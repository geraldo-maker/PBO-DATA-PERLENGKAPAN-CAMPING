class Peralatan:
    def __init__(self, kode, nama, kategori, jumlah, kondisi):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.jumlah = int(jumlah)
        self.kondisi = kondisi

    def to_list(self):
        return [
            self.kode, self.nama, self.kategori,
            self.jumlah, self.kondisi
        ]

