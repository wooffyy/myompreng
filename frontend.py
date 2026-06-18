import tkinter as tk
from tkinter import ttk, messagebox

import backend


class MenuOptimizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Optimasi Menu MBG")
        self.resizable(False, False)
        self._create_widgets()

    def _create_widgets(self):
        self._create_parameter_section()
        self._create_statistics_section()
        self._create_results_section()

    def _create_parameter_section(self):
        parameter_frame = ttk.LabelFrame(self, text="Parameter")
        parameter_frame.grid(row=0, column=0, padx=12, pady=12, sticky="ew")

        ttk.Label(parameter_frame, text="Max Budget").grid(row=0, column=0, sticky="w", pady=4)
        self.max_budget_var = tk.StringVar()
        self.max_budget_entry = ttk.Entry(parameter_frame, textvariable=self.max_budget_var)
        self.max_budget_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

        ttk.Label(parameter_frame, text="Min Kalori").grid(row=1, column=0, sticky="w", pady=4)
        self.min_calorie_var = tk.StringVar()
        self.min_calorie_entry = ttk.Entry(parameter_frame, textvariable=self.min_calorie_var)
        self.min_calorie_entry.grid(row=1, column=1, sticky="ew", padx=8, pady=4)

        ttk.Label(parameter_frame, text="Max Kalori").grid(row=2, column=0, sticky="w", pady=4)
        self.max_calorie_var = tk.StringVar()
        self.max_calorie_entry = ttk.Entry(parameter_frame, textvariable=self.max_calorie_var)
        self.max_calorie_entry.grid(row=2, column=1, sticky="ew", padx=8, pady=4)

        parameter_frame.columnconfigure(1, weight=1)

        run_button = ttk.Button(parameter_frame, text="Jalankan", command=self._on_run_clicked)
        run_button.grid(row=3, column=0, columnspan=2, pady=(8, 4), sticky="ew")

    def _create_statistics_section(self):
        stats_frame = ttk.LabelFrame(self, text="Statistik Algoritma")
        stats_frame.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="ew")

        ttk.Label(stats_frame, text="Node Dieksplorasi:").grid(row=0, column=0, sticky="w", pady=4)
        self.nodes_explored_value = ttk.Label(stats_frame, text="-")
        self.nodes_explored_value.grid(row=0, column=1, sticky="e", pady=4)

        ttk.Label(stats_frame, text="Branch Dipangkas:").grid(row=1, column=0, sticky="w", pady=4)
        self.branches_pruned_value = ttk.Label(stats_frame, text="-")
        self.branches_pruned_value.grid(row=1, column=1, sticky="e", pady=4)

        ttk.Label(stats_frame, text="Solusi Ditemukan (dari eksplorasi terbatas): ").grid(row=2, column=0, sticky="w", pady=4)
        self.valid_solutions_value = ttk.Label(stats_frame, text="-")
        self.valid_solutions_value.grid(row=2, column=1, sticky="e", pady=4)

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

    def _create_results_section(self):
        results_frame = ttk.LabelFrame(self, text="Hasil Kombinasi Menu")
        results_frame.grid(row=2, column=0, padx=12, pady=(0, 12), sticky="nsew")

        columns = [
            "hari_ke",
            "karbohidrat",
            "protein_hewani",
            "protein_nabati",
            "sayur",
            "buah",
            "total_harga",
            "total_kalori",
        ]

        self.tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            height=8,
        )

        self.tree.heading("hari_ke", text="Hari Ke")
        self.tree.heading("karbohidrat", text="Karbohidrat")
        self.tree.heading("protein_hewani", text="Protein Hewani")
        self.tree.heading("protein_nabati", text="Protein Nabati")
        self.tree.heading("sayur", text="Sayur")
        self.tree.heading("buah", text="Buah")
        self.tree.heading("total_harga", text="Total Harga")
        self.tree.heading("total_kalori", text="Total Kalori")

        self.tree.column("hari_ke", width=70, anchor="center")
        self.tree.column("karbohidrat", width=140, anchor="w")
        self.tree.column("protein_hewani", width=140, anchor="w")
        self.tree.column("protein_nabati", width=140, anchor="w")
        self.tree.column("sayur", width=120, anchor="w")
        self.tree.column("buah", width=120, anchor="w")
        self.tree.column("total_harga", width=100, anchor="e")
        self.tree.column("total_kalori", width=100, anchor="e")

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

    def _on_run_clicked(self):
        try:
            max_budget = self._parse_positive_int(self.max_budget_var.get(), "Max Budget")
            min_calorie = self._parse_non_negative_int(self.min_calorie_var.get(), "Min Kalori")
            max_calorie = self._parse_non_negative_int(self.max_calorie_var.get(), "Max Kalori")

            if max_calorie < min_calorie:
                raise ValueError("Max Kalori harus lebih besar atau sama dengan Min Kalori.")

            self._run_backend(max_budget, min_calorie, max_calorie)
        except ValueError as exc:
            messagebox.showerror("Input Tidak Valid", str(exc))

    def _parse_positive_int(self, value, label):
        if not value.strip():
            raise ValueError(f"{label} harus diisi.")
        try:
            parsed = int(value)
        except ValueError:
            raise ValueError(f"{label} harus berupa angka bulat.")
        if parsed <= 0:
            raise ValueError(f"{label} harus lebih besar dari 0.")
        return parsed

    def _parse_non_negative_int(self, value, label):
        if not value.strip():
            raise ValueError(f"{label} harus diisi.")
        try:
            parsed = int(value)
        except ValueError:
            raise ValueError(f"{label} harus berupa angka bulat.")
        if parsed < 0:
            raise ValueError(f"{label} tidak boleh negatif.")
        return parsed

    def _run_backend(self, max_budget, min_calorie, max_calorie):
        try:
            result = backend.cari_jadwal(
                max_budget,
                min_calorie,
                max_calorie,
                5,
                backend.data,
            )
        except Exception as exc:
            messagebox.showerror("Backend Error", str(exc))
            return

        self._update_statistics(result)
        self._update_results(result)

    def _update_statistics(self, result):
        stats = result.get("stats", {})
        self.nodes_explored_value.config(text=str(stats.get("node", "-")))
        self.branches_pruned_value.config(text=str(stats.get("prune", "-")))
        self.valid_solutions_value.config(text=str(len(result.get("solutions", []))))

    def _update_results(self, result):
        for row in self.tree.get_children():
            self.tree.delete(row)

        solutions = result.get("solutions", [])
        if not solutions:
            return

        first_solution = solutions[0]
        for hari_ke, menu in enumerate(first_solution, start=1):
            self.tree.insert(
                "",
                "end",
                values=[
                    hari_ke,
                    menu.get("karbo", {}).get("nama", ""),
                    menu.get("protein_h", {}).get("nama", ""),
                    menu.get("protein_n", {}).get("nama", ""),
                    menu.get("sayur", {}).get("nama", ""),
                    menu.get("buah", {}).get("nama", ""),
                    menu.get("total_harga", ""),
                    menu.get("total_kalori", ""),
                ],
            )


def main():
    app = MenuOptimizerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
