import csv
import os
from models import Peralatan

FILE_DATA = "peralatan.csv"
HEADER = ["Kode", "Nama", "Kategori", "Jumlah", "Kondisi"]

def tambah_peralatan():
    print("\n=== TAMBAH PERALATAN CAMPING ===")
    kode = input("Kode peralatan : ").strip().upper()
    nama = input("Nama peralatan : ").strip()
    kategori = input("Kategori       : ").strip()
    jumlah_text = input("Jumlah         : ").strip()
    kondisi = input("Kondisi        : ").strip()

    if not all([kode, nama, kategori, jumlah_text, kondisi]):
        print("Semua kolom wajib diisi.")
        return

    try:
        jumlah = int(jumlah_text)
        if jumlah < 0:
            print("Jumlah tidak boleh negatif.")
            return
    except ValueError:
        print("Jumlah harus berupa bilangan bulat.")
        return

    file_ada = os.path.exists(FILE_DATA)
    if file_ada and os.path.getsize(FILE_DATA) > 0:
        with open(FILE_DATA, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if any(row["Kode"].strip().upper() == kode for row in reader):
                print("Kode tersebut sudah digunakan.")
                return

    item = Peralatan(kode, nama, kategori, jumlah, kondisi)
    with open(FILE_DATA, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_ada or os.path.getsize(FILE_DATA) == 0:
            writer.writerow(HEADER)
        writer.writerow(item.to_list())

    print("Data peralatan berhasil disimpan.")

if __name__ == "__main__":
    tambah_peralatan()
