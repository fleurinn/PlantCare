import json
from datetime import datetime
from tabulate import tabulate

DATA_FILE = "jagung_ketan.json"
# ADMIN_PATH = "../json/admin.json"
# SPESIFIKASI_PATH = "../json/spesifikasi.json"

# code untuk penyimpanan ke database
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# standar tinggi pertumbuhan berdasarkan hari
STANDAR_TINGGI = {
    7: (10, 15),
    14: (25, 35),
    21: (40, 60),
    30: (70, 100),
    45: (120, 160),
    60: (180, 220),
}

def analisis_tinggi(umur, tinggi):
    if umur not in STANDAR_TINGGI:
        return "Belum ada data standar untuk umur ini."
    
    batas_bawah, batas_atas = STANDAR_TINGGI[umur]

    if tinggi < batas_bawah:
        return f"Terlalu pendek. Ideal: {batas_bawah}-{batas_atas} cm."
    elif tinggi > batas_atas:
        return f"Lebih tinggi dari rata-rata. Ideal: {batas_bawah}-{batas_atas} cm."
    else:
        return f"Normal (Ideal: {batas_bawah}-{batas_atas} cm)."

def analisis_suhu(suhu):
    if suhu < 24:
        return "Terlalu dingin (ideal 24–30°C)."
    elif suhu > 30:
        return "Terlalu panas (ideal 24–30°C)."
    return "Suhu ideal."

def analisis_lembap(lembap):
    if lembap < 60:
        return "Kekurangan air (ideal 60–80%)."
    elif lembap > 80:
        return "Terlalu basah (ideal 60–80%)."
    return "Kelembapan ideal."

def analisis_daun(daun):
    if daun.lower() == "hijau":
        return "Daun sehat."
    return "Daun tidak sehat — mungkin ada penyakit atau kekurangan nutrisi."

# =====================
# CRUD
# =====================
def tambah_catatan(data):
    print("\n=== Tambah Catatan Pertumbuhan Jagung Ketan ===")

    tanggal = datetime.now().strftime("%Y-%m-%d")
    umur = int(input("Umur tanaman (hari): "))
    tinggi = float(input("Tinggi (cm): "))
    suhu = float(input("Suhu lingkungan (°C): "))
    lembap = float(input("Kelembapan (%): "))
    daun = input("Kondisi daun (hijau/kering/rusak): ")

    catatan = {
        "tanggal": tanggal,
        "umur": umur,
        "tinggi": tinggi,
        "suhu": suhu,
        "lembap": lembap,
        "daun": daun
    }

    data.append(catatan)
    save_data(data)

    print("\n=== Analisis Pertumbuhan ===")
    print("Tinggi :", analisis_tinggi(umur, tinggi))
    print("Suhu   :", analisis_suhu(suhu))
    print("Lembap :", analisis_lembap(lembap))
    print("Daun   :", analisis_daun(daun))


def lihat_data(data):
    if not data:
        print("Belum ada catatan.")
        return
    
    tampilkan_tabel(data)

# =====================
# SEARCHING
# =====================
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

# =====================
# SORTING
# =====================
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

# =====================
# UPDATE
# =====================
def update_data(data):
    if not data:
        print("Belum ada catatan.")
        return

    tampilkan_tabel(data)

    try:
        index = int(input("Pilih nomor catatan yang ingin diupdate: ")) - 1
        if index < 0 or index >= len(data):
            print("Nomor tidak valid.")
            return
    except:
        print("Input harus angka.")
        return

    catatan = data[index]
    print("\n=== Update Catatan ===")
    print("Tekan ENTER jika tidak ingin mengubah nilai.")

    new_tinggi = input(f"Tinggi baru (cm) [{catatan['tinggi']}]: ")
    new_suhu = input(f"Suhu baru (°C) [{catatan['suhu']}]: ")
    new_lembap = input(f"Kelembapan baru (%) [{catatan['lembap']}]: ")
    new_daun = input(f"Kondisi daun baru [{catatan['daun']}]: ")

    if new_tinggi:
        catatan["tinggi"] = float(new_tinggi)
    if new_suhu:
        catatan["suhu"] = float(new_suhu)
    if new_lembap:
        catatan["lembap"] = float(new_lembap)
    if new_daun:
        catatan["daun"] = new_daun

    save_data(data)
    print("Catatan berhasil diperbarui!")

# =====================
# DELETE
# =====================
def delete_data(data):
    if not data:
        print("Belum ada catatan.")
        return

    tampilkan_tabel(data)

    try:
        index = int(input("Pilih nomor catatan yang ingin dihapus: ")) - 1
        if index < 0 or index >= len(data):
            print("Nomor tidak valid.")
            return
    except:
        print("Input harus angka.")
        return

    konfirmasi = input("Yakin ingin menghapus? (y/n): ")

    if konfirmasi.lower() == "y":
        data.pop(index)
        save_data(data)
        print("Catatan berhasil dihapus!")
    else:
        print("Penghapusan dibatalkan.")

# =====================
# Utility tabel
# =====================
def tampilkan_tabel(records):
    tabel = [
        [i+1, d["tanggal"], d["umur"], d["tinggi"], d["suhu"], d["lembap"], d["daun"]]
        for i, d in enumerate(records)
    ]

    print(tabulate(
        tabel,
        headers=["No", "Tanggal", "Umur (hari)", "Tinggi", "Suhu", "Lembap", "Daun"],
        tablefmt="grid"
    ))

# =====================
# MENU UTAMA
# =====================
def main():
    data = load_data()

    while True:
        print("\n🌽 SISTEM MONITORING JAGUNG KETAN 🌽")
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
