from backend import cari_jadwal, data
import json

max_budget=15000
min_kal=650
max_kal=750 
jumlah_hari=5 
data=data
print("Parameter: max_budget=",max_budget, "min_kal=",min_kal, "max_kal=",max_kal, "jumlah_hari=",jumlah_hari)
result = cari_jadwal(max_budget, min_kal, max_kal, jumlah_hari, data)


# Cetak statistik pruning dan jumlah solusi yang ditemukan
print("=== STATISTIK BACKTRACKING ===")
print(f"Total Kombinasi Dicek (Node): {result['stats']['node']}")
print(f"Prune (Harga/Kalori)        : {result['stats']['prune']}")
print(f"Prune Early (Subtotal)      : {result['stats']['prune_early']}")
print(f"Prune Variasi (Menu Sama)   : {result['stats']['prune_variasi']}")
print(f"Jumlah Solusi Ditemukan     : {len(result['solutions'])}")
print("=============================\n")

# Cetak salah satu contoh solusi jika ada (biar terminal gak penuh)
if result['solutions']:
    # Kita ambil contoh solusi pertama (indeks 0)
    solusi_terpilih = result['solutions'][0]
    
    print(f"=== REKOMENDASI JADWAL MENU (5 HARI) ===")
    
    # Looping untuk mencetak hari ke-1 sampai hari ke-5
    for hari_ke, menu in enumerate(solusi_terpilih, start=1):
        print(f"\nHARI KE-{hari_ke}")
        print(f"  Karbohidrat : {menu['karbo']['nama']} (Rp{menu['karbo']['harga_per_porsi']} | {menu['karbo']['kalori']} kkal)")
        print(f"  Protein H   : {menu['protein_h']['nama']} (Rp{menu['protein_h']['harga_per_porsi']} | {menu['protein_h']['kalori']} kkal)")
        print(f"  Protein N   : {menu['protein_n']['nama']} (Rp{menu['protein_n']['harga_per_porsi']} | {menu['protein_n']['kalori']} kkal)")
        print(f"  Sayur       : {menu['sayur']['nama']} (Rp{menu['sayur']['harga_per_porsi']} | {menu['sayur']['kalori']} kkal)")
        print(f"  Buah        : {menu['buah']['nama']} (Rp{menu['buah']['harga_per_porsi']} | {menu['buah']['kalori']} kkal)")
        print(f"  ---------")
        print(f"  Total Harga  : Rp{menu['total_harga']}")
        print(f"  Total Kalori : {menu['total_kalori']} kkal")
        
    print("\n=========================================")
else:
    print("❌ Tidak ada kombinasi jadwal 5 hari yang memenuhi budget dan kalori.")