import json
import random

def cari_jadwal(max_budget, min_kal, max_kal, jumlah_hari, data):
    hasil = []
    stats = {"node": 0, "prune": 0, "prune_variasi": 0, "prune_early": 0}

    def _backtrack(hari_ke, jadwal):
        if len(hasil) >= 1000000:  
            return
        
        if hari_ke == jumlah_hari:
            hasil.append([m.copy() for m in jadwal])
            return

        protein_kemarin = None
        if jadwal:
            prev = jadwal[-1]
            protein_kemarin = (prev["protein_h"]["nama"], prev["protein_n"]["nama"])

        # === SOLUSI: Mengacak urutan iterasi secara dinamis di setiap hari ===
        # random.sample(list, len(list)) akan mengembalikan list baru yang teracak tanpa mengubah data asli
        
        karbo_shuffled = random.sample(data["Karbo"], len(data["Karbo"]))
        ph_shuffled = random.sample(data["ProteinH"], len(data["ProteinH"]))
        pn_shuffled = random.sample(data["ProteinN"], len(data["ProteinN"]))

        for karbo in karbo_shuffled:
            for ph in ph_shuffled:
                for pn in pn_shuffled:
                    if protein_kemarin == (ph["nama"], pn["nama"]):
                        stats["prune_variasi"] += 1
                        continue
                    
                    subtotal_harga = karbo["harga_per_porsi"] + ph["harga_per_porsi"] + pn["harga_per_porsi"]
                    if subtotal_harga > max_budget:
                        stats["prune_early"] += 1
                        continue
                    
                    # Acak juga untuk Sayur dan Buah di dalam loop
                    sayur_shuffled = random.sample(data["Sayur"], len(data["Sayur"]))
                    buah_shuffled = random.sample(data["Buah"], len(data["Buah"]))

                    for sayur in sayur_shuffled:
                        for buah in buah_shuffled:
                            stats["node"] += 1
                            total_harga  = subtotal_harga + sayur["harga_per_porsi"] + buah["harga_per_porsi"]
                            total_kalori = karbo["kalori"] + ph["kalori"] + pn["kalori"] + sayur["kalori"] + buah["kalori"]

                            if total_harga > max_budget:
                                stats["prune"] += 1
                                continue
                            if total_kalori > max_kal:
                                stats["prune"] += 1
                                continue
                            if total_kalori < min_kal:
                                continue
                            
                            menu = {
                                "karbo": karbo, "protein_h": ph, "protein_n": pn,
                                "sayur": sayur, "buah": buah, "total_harga": total_harga, 
                                "total_kalori": total_kalori
                            }
                            jadwal.append(menu)
                            _backtrack(hari_ke + 1, jadwal)
                            jadwal.pop()

    _backtrack(0, [])
    return {"solutions": hasil, "stats": stats}


with open("dataset.json", "r") as f:
    data = json.load(f)