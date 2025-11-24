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


# standar per minggu (1-14) berdasarkan data pertumbuhan
STANDAR_MINGGU = {
    1:  {"umur_days": (0, 7),   "tinggi_cm": (5, 10),    "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (0, 1)},
    2:  {"umur_days": (8, 14),  "tinggi_cm": (20, 30),   "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (4, 6)},
    3:  {"umur_days": (15, 21), "tinggi_cm": (45, 55),   "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (6, 8)},
    4:  {"umur_days": (22, 28), "tinggi_cm": (70, 80),   "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (7, 9)},
    5:  {"umur_days": (29, 35), "tinggi_cm": (95, 105),  "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (8, 10)},
    6:  {"umur_days": (36, 42), "tinggi_cm": (140, 160), "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (10, 11)},
    7:  {"umur_days": (43, 49), "tinggi_cm": (160, 180), "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (11, 12)},
    8:  {"umur_days": (50, 56), "tinggi_cm": (185, 195), "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (11, 13)},
    9:  {"umur_days": (57, 63), "tinggi_cm": (195, 205), "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (11, 13)},
    10: {"umur_days": (64, 70), "tinggi_cm": (195, 205), "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (11, 13)},
    11: {"umur_days": (71, 77), "tinggi_cm": (195, 205), "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (11, 13)},
    12: {"umur_days": (78, 84), "tinggi_cm": (180, 200), "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (11, 13), "status": "mengering"},
    13: {"umur_days": (85, 91), "tinggi_cm": (160, 190), "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (0, 12),  "status": "mengering"},
    14: {"umur_days": (92, 98), "tinggi_cm": (150, 190), "suhu_C": (23, 27), "lembap_pct": (75, 85), "daun": (0, 12),  "status": "panen"},
}

def _find_week_by_day(umur_hari):
    for minggu, data in STANDAR_MINGGU.items():
        low, high = data["umur_days"]
        if low <= umur_hari <= high:
            return minggu, data
    return None, None

def analisis_tinggi(umur_hari, tinggi_cm):
    minggu, standar = _find_week_by_day(umur_hari)
    if not standar:
        return "Belum ada data standar untuk umur ini."
    low, high = standar["tinggi_cm"]
    if tinggi_cm < low:
        return f"Terlalu pendek. Ideal minggu {minggu}: {low}-{high} cm."
    if tinggi_cm > high:
        return f"Lebih tinggi dari rata-rata. Ideal minggu {minggu}: {low}-{high} cm."
    return f"Normal (Minggu {minggu}, Ideal: {low}-{high} cm)."

def analisis_suhu(umur_hari, suhu_C):
    minggu, standar = _find_week_by_day(umur_hari)
    if not standar:
        return "Belum ada data standar suhu untuk umur ini."
    low, high = standar["suhu_C"]
    if suhu_C < low:
        return f"Terlalu dingin untuk minggu {minggu} (ideal {low}–{high}°C)."
    if suhu_C > high:
        return f"Terlalu panas untuk minggu {minggu} (ideal {low}–{high}°C)."
    return f"Suhu ideal untuk minggu {minggu} ({low}–{high}°C)."

def analisis_lembap(umur_hari, lembap_pct):
    minggu, standar = _find_week_by_day(umur_hari)
    if not standar:
        return "Belum ada data standar kelembapan untuk umur ini."
    low, high = standar["lembap_pct"]
    if lembap_pct < low:
        return f"Kekurangan air untuk minggu {minggu} (ideal ~{low}–{high}%)."
    if lembap_pct > high:
        return f"Terlalu basah untuk minggu {minggu} (ideal ~{low}–{high}%)."
    return f"Kelembapan ideal untuk minggu {minggu} (sekitar {low}–{high}%)."

def analisis_daun(umur_hari, daun):
    minggu, standar = _find_week_by_day(umur_hari)
    if not standar:
        return "Belum ada data standar daun untuk umur ini."

    expected_low, expected_high = standar["daun"]
    status = standar.get("status", "")
    desc = str(daun).lower()

    # jika user tulis angka, misal "5"
    daun_num = None
    if desc.replace('.', '', 1).isdigit():
        daun_num = float(desc)

    if daun_num is not None:
        if daun_num < expected_low:
            return f"Jumlah daun ({daun_num}) lebih sedikit dari yang diharapkan minggu {minggu} (ideal ~{expected_low}-{expected_high} helai)."
        if daun_num > expected_high:
            return f"Jumlah daun ({daun_num}) lebih banyak dari tipikal minggu {minggu} (ideal ~{expected_low}-{expected_high} helai)."
        if status in ("mengering", "panen"):
            return f"Jumlah daun {daun_num} helai; pada minggu {minggu} tanaman memasuki fase '{status}' (daun mungkin mengering)."
        return f"Jumlah daun normal untuk minggu {minggu} (sekitar {expected_low}-{expected_high} helai)."

    # jika deskriptif
    if "hijau" in desc:
        return f"Daun hijau — tanda sehat untuk minggu {minggu} (ideal ~{expected_low}-{expected_high} helai)."
    if "kering" in desc:
        if status in ("mengering", "panen"):
            return f"Daun kering — sesuai fase '{status}' (mendekati panen) di minggu {minggu}."
        return f"Daun kering — bisa jadi stres air/nutrisi pada minggu {minggu}."
    if "rusak" in desc:
        return f"Daun rusak — kemungkinan gangguan hama/penyakit pada minggu {minggu}."

    return f"Kondisi daun '{daun}' dicatat. Rentang daun tipikal minggu {minggu}: ~{expected_low}-{expected_high} helai."

# mengembalikan ringkasan analisis dari dict berdasarkan input yang diberikan.
def analisis_keseluruhan(umur_hari, tinggi_cm=None, suhu_C=None, lembap_pct=None, daun=None):
    minggu, standar = _find_week_by_day(umur_hari)
    if not standar:
        return {"error": "Belum ada data standar untuk umur ini."}
    hasil = {
        "minggu": minggu,
        "standar": standar
    }
    if tinggi_cm is not None:
        hasil["tinggi"] = analisis_tinggi(umur_hari, tinggi_cm)
    if suhu_C is not None:
        hasil["suhu"] = analisis_suhu(umur_hari, suhu_C)
    if lembap_pct is not None:
        hasil["kelembapan"] = analisis_lembap(umur_hari, lembap_pct)
    if daun is not None:
        hasil["daun"] = analisis_daun(umur_hari, daun)
    return hasil


# CREATE
def tambah_catatan(data):
    print("\n=== Tambah Catatan Pertumbuhan Jagung Ketan ===")

    tanggal = datetime.now().strftime("%Y-%m-%d")
    umur = int(input("Umur tanaman (hari): "))
    tinggi = float(input("Tinggi (cm): "))
    suhu = float(input("Suhu lingkungan (°C): "))
    lembap = float(input("Kelembapan (%): "))
    daun = input("Kondisi daun (hijau/kering/rusak atau angka jumlah helai): ")

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
    ringkasan = analisis_keseluruhan(
        umur_hari=umur,
        tinggi_cm=tinggi,
        suhu_C=suhu,
        lembap_pct=lembap,
        daun=daun
    )

    if "error" in ringkasan:
        print(ringkasan["error"])
    else:
        print(f"Minggu ke-{ringkasan['minggu']} (standar umur hari: {ringkasan['standar']['umur_days'][0]}–{ringkasan['standar']['umur_days'][1]})")
        print("Tinggi :", ringkasan.get("tinggi", "-"))
        print("Suhu   :", ringkasan.get("suhu", "-"))
        print("Lembap :", ringkasan.get("kelembapan", "-"))
        print("Daun   :", ringkasan.get("daun", "-"))

# READ
def lihat_data(data):
    if not data:
        print("Belum ada catatan.")
        return
    
    tampilkan_tabel(data)

# SEARCH DATA (CARI DATA BERDASARKAN TANGGAL DAN UMUR TANAMAN)
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


# SORTING DATA BERDASARKAN 
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

# UPDATE
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

# DELETE
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


# MENAMMPILKAN TABEL MENGGUNAKAN TABULATE
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

# MENU UTAMA
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
