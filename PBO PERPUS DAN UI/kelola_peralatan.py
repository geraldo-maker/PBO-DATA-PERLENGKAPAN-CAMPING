import csv
import os
from models import Peralatan

FILE_DATA = "peralatan.csv"

def muat_data():
    daftar = []
    if not os.path.exists(FILE_DATA):
        return daftar
    with open(FILE_DATA, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            daftar.append(Peralatan(
                row["Kode"], row["Nama"], row["Kategori"],
                row["Jumlah"], row["Kondisi"]
            ))
    return daftar

def tampilkan_peralatan():
    daftar = muat_data()
    if not daftar:
        print("Belum ada data peralatan.")
        return
    print("\n=== DAFTAR PERALATAN CAMPING ===")
    print(f"{'Kode':12}{'Nama':22}{'Kategori':24}{'Jumlah':9}Kondisi")
    print("-" * 90)
    for item in daftar:
        print(f"{item.kode:12}{item.nama:22}{item.kategori:24}"
              f"{item.jumlah:<9}{item.kondisi}")
    print("-" * 90)
    print(f"Jumlah jenis peralatan: {len(daftar)}")

def cari_peralatan():
    kode = input("Masukkan kode peralatan: ").strip().upper()
    for item in muat_data():
        if item.kode == kode:
            print("\nData ditemukan:")
            print(f"Kode     : {item.kode}")
            print(f"Nama     : {item.nama}")
            print(f"Kategori : {item.kategori}")
            print(f"Jumlah   : {item.jumlah}")
            print(f"Kondisi  : {item.kondisi}")
            return
    print("Peralatan dengan kode tersebut tidak ditemukan.")

if __name__ == "__main__":
    print("\n=== KELOLA DATA PERALATAN ===")
    print("1. Tampilkan semua peralatan")
    print("2. Cari peralatan berdasarkan kode")
    pilihan = input("Pilih menu: ").strip()
    if pilihan == "1":
        tampilkan_peralatan()
    elif pilihan == "2":
        cari_peralatan()
    else:
        print("Pilihan tidak valid.")
