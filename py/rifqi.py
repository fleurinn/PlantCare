def search_data(data):
    if not data:
        print("Belum ada catatan.")
        return

    print("\nCari berdasarkan:")
    print("1. Tanggal (YYYY-MM-DD)")
    print("2. Umur (hari)")
    
    pilih = input("Pilih: ")

    if pilih == "1":
        keyword = input("Masukkan tanggal: ")
        hasil = [d for d in data if keyword in d["tanggal"]]
    elif pilih == "2":
        try:
            umur = int(input("Masukkan umur: "))
            hasil = [d for d in data if d["umur"] == umur]
        except:
            print("Umur harus angka.")
            return
    else:
        print("Pilihan tidak valid.")
        return
    
    if hasil:
        print("\n=== Hasil Pencarian ===")
        tampilkan_tabel(hasil)
    else:
        print("Tidak ditemukan.")


def sort_data(data):
    if not data:
        print("Belum ada catatan.")
        return

    print("\nSort berdasarkan:")
    print("1. Tanggal")
    print("2. Umur")
    print("3. Tinggi")
    print("4. Suhu")
    print("5. Kelembapan")

    pilih = input("Pilih: ")

    key_map = {
        "1": "tanggal",
        "2": "umur",
        "3": "tinggi",
        "4": "suhu",
        "5": "lembap",
    }

    if pilih not in key_map:
        print("Pilihan tidak valid.")
        return

    key = key_map[pilih]

    if key == "tanggal":
        data.sort(key=lambda x: datetime.strptime(x["tanggal"], "%Y-%m-%d"))
    else:
        data.sort(key=lambda x: x[key])

    print("\n=== Data Setelah Sorting ===")
    tampilkan_tabel(data)
    save_data(data)


def main():
    data = load_data()

    while True:
        print("\n SISTEM MONITORING JAGUNG KETAN")
        print("1. Tambah catatan pertumbuhan")
        print("2. Lihat semua catatan")
        print("3. Search catatan")
        print("4. Sort catatan")
        print("5. Update catatan")
        print("6. Hapus catatan")
        print("0. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_catatan(data)
        elif pilih == "2":
            lihat_data(data)
        elif pilih == "3":
            search_data(data)
        elif pilih == "4":
            sort_data(data)
        elif pilih == "5":
            update_data(data)
        elif pilih == "6":
            delete_data(data)
        elif pilih == "0":
            print("Sampai jumpa 🌱")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()

print('Hello World!')