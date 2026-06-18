import json
import random

def cari_jadwal(max_budget, min_kal, max_kal, jumlah_hari, data):
    hasil = []
    stats = {"node": 0, "prune": 0, "prune_variasi": 0, "prune_early": 0}

    def _backtrack(hari_ke, jadwal):
        if len(hasil) >= 100000:
            return

        if hari_ke == jumlah_hari:
            hasil.append([m.copy() for m in jadwal])
            return

        protein_kemarin = None
        protein_2hari_lalu = None
        pn_kemarin = None

        if len(jadwal) >= 1:
            protein_kemarin = jadwal[-1]["protein_h"]["nama"]
            pn_kemarin = jadwal[-1]["protein_n"]["nama"]

        if len(jadwal) >= 2:
            protein_2hari_lalu = jadwal[-2]["protein_h"]["nama"]

        karbo_list = random.sample(data["Karbo"], len(data["Karbo"]))
        ph_list    = random.sample(data["ProteinH"], len(data["ProteinH"]))
        pn_list    = random.sample(data["ProteinN"], len(data["ProteinN"]))
        sayur_list = random.sample(data["Sayur"], len(data["Sayur"]))
        buah_list  = random.sample(data["Buah"], len(data["Buah"]))

        for karbo in karbo_list:
            for ph in ph_list:

                if ph["nama"] == protein_kemarin:
                    stats["prune_variasi"] += 1
                    continue
                if ph["nama"] == protein_2hari_lalu:
                    stats["prune_variasi"] += 1
                    continue

                for pn in pn_list:
                    subtotal_harga = karbo["harga_per_porsi"] + ph["harga_per_porsi"] + pn["harga_per_porsi"]
                    if pn["nama"] == pn_kemarin:
                        stats["prune_variasi"] += 1
                        continue
                    if subtotal_harga > max_budget:
                        stats["prune_early"] += 1
                        continue

                    for sayur in sayur_list:
                        for buah in buah_list:
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
                                "sayur": sayur, "buah": buah,
                                "total_harga": total_harga, "total_kalori": total_kalori
                            }
                            jadwal.append(menu)
                            _backtrack(hari_ke + 1, jadwal)
                            jadwal.pop()
    _backtrack(0, [])
    return {"solutions": hasil, "stats": stats}


with open("dataset.json", "r") as f:
    data = json.load(f)