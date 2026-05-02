import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import borshtanga_core

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class BorshtangaApp:
    """Класс главного окна приложения."""

    def __init__(self, root):
        self.root = root
        self.root.title("Устойчивость расточной борштанги — D-разбиение")
        self.root.geometry("1200x750")

        # Список кривых, построенных пользователем (для накопления и сравнения)
        self.curves = []  # [(params_dict, points), ...]

        self._create_widgets()

    # ========== Создание интерфейса ==========

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ===== ЛЕВАЯ ПАНЕЛЬ: ввод параметров =====
        params_frame = ttk.LabelFrame(main_frame, text="Параметры системы", padding=10)
        params_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.param_specs = [
            ("G",      "8.0e10",  "Модуль сдвига G, Н/м²"),
            ("rho",    "7800",    "Плотность ρ, кг/м³"),
            ("Jp",     "1.9e-5",  "Полярный момент инерции Jₚ, м⁴"),
            ("Jr",     "2.57e-2", "Момент инерции головки Jᵣ, кг·м²"),
            ("L",      "2.5",     "Длина борштанги L, м"),
            ("delta1", "1.0e-5",  "Коэффициент трения δ₁"),
        ]

        self.entries = {}

        for i, (name, default, label) in enumerate(self.param_specs):
            ttk.Label(params_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(params_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.entries[name] = entry

        # Параметры расчёта
        ttk.Separator(params_frame, orient=tk.HORIZONTAL).grid(
            row=len(self.param_specs), column=0, columnspan=2, sticky=tk.EW, pady=10
        )
        ttk.Label(params_frame, text="Параметры расчёта:", font=("", 9, "bold")).grid(
            row=len(self.param_specs) + 1, column=0, columnspan=2, sticky=tk.W
        )

        self.curve_specs = [
            ("omega_min",  "-1000", "ω мин"),
            ("omega_max",   "1000", "ω макс"),
            ("num_points",  "5000", "Число точек"),
            ("hatch_step",   "100", "Шаг штриховки"),
        ]

        for i, (name, default, label) in enumerate(self.curve_specs):
            row = len(self.param_specs) + 2 + i
            ttk.Label(params_frame, text=label).grid(row=row, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(params_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=row, column=1, padx=5, pady=3)
            self.entries[name] = entry

        # Кнопки
        btn_row = len(self.param_specs) + 2 + len(self.curve_specs)

        ttk.Button(
            params_frame, text="Добавить кривую D-разбиения",
            command=self.add_d_curve
        ).grid(row=btn_row, column=0, columnspan=2, pady=(15, 3), sticky=tk.EW)

        ttk.Button(
            params_frame, text="Очистить все кривые",
            command=self.clear_curves
        ).grid(row=btn_row + 1, column=0, columnspan=2, pady=3, sticky=tk.EW)

        ttk.Separator(params_frame, orient=tk.HORIZONTAL).grid(
            row=btn_row + 2, column=0, columnspan=2, sticky=tk.EW, pady=10
        )

        ttk.Button(
            params_frame, text="Построить диаграмму устойчивости",
            command=self.plot_stability_diagram
        ).grid(row=btn_row + 3, column=0, columnspan=2, pady=3, sticky=tk.EW)

        ttk.Separator(params_frame, orient=tk.HORIZONTAL).grid(
            row=btn_row + 4, column=0, columnspan=2, sticky=tk.EW, pady=10
        )

        ttk.Button(
            params_frame, text="Сохранить текущий график",
            command=self.save_current_plot
        ).grid(row=btn_row + 5, column=0, columnspan=2, pady=3, sticky=tk.EW)

        # ===== ПРАВАЯ ПАНЕЛЬ: вкладки с графиками =====
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка 1: D-кривая
        self.tab_dcurve = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_dcurve, text="Кривая D-разбиения")
        self._create_dcurve_tab()

        # Вкладка 2: Диаграмма устойчивости
        self.tab_stability = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stability, text="Диаграмма устойчивости")
        self._create_stability_tab()

    def _create_dcurve_tab(self):
        self.fig_d = Figure(figsize=(8, 6), dpi=100)
        self.ax_d = self.fig_d.add_subplot(111)
        self._setup_dcurve_axes()

        self.canvas_d = FigureCanvasTkAgg(self.fig_d, master=self.tab_dcurve)
        self.canvas_d.draw()
        self.canvas_d.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas_d, self.tab_dcurve)
        toolbar.update()

    def _create_stability_tab(self):
        self.fig_s = Figure(figsize=(8, 6), dpi=100)
        self.ax_s = self.fig_s.add_subplot(111)
        self._setup_stability_axes()

        self.canvas_s = FigureCanvasTkAgg(self.fig_s, master=self.tab_stability)
        self.canvas_s.draw()
        self.canvas_s.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas_s, self.tab_stability)
        toolbar.update()

    def _setup_dcurve_axes(self):
        self.ax_d.clear()
        self.ax_d.set_title("Кривая D-разбиения")
        self.ax_d.set_xlabel(r"$\mathrm{Re}\,\hat{\delta}$")
        self.ax_d.set_ylabel(r"$\mathrm{Im}\,\hat{\delta}$")
        self.ax_d.grid(True, linestyle="--", alpha=0.5)
        self.ax_d.axhline(0, color="black", linewidth=0.5)
        self.ax_d.axvline(0, color="black", linewidth=0.5)

    def _setup_stability_axes(self):
        self.ax_s.clear()
        self.ax_s.set_title("Диаграмма устойчивости")
        self.ax_s.set_xlabel(r"$\delta$")
        self.ax_s.set_ylabel(r"$\delta_1$")
        self.ax_s.grid(True, linestyle="--", alpha=0.5)
        self.ax_s.axhline(0, color="black", linewidth=0.5)
        self.ax_s.axvline(0, color="black", linewidth=0.5)

    # ========== Чтение параметров ==========

    def _read_params(self):
        """Считывает параметры из формы. Возвращает словарь или None при ошибке."""
        try:
            params = borshtanga_core.BorshtangaParams()
            params.G      = float(self.entries["G"].get())
            params.rho    = float(self.entries["rho"].get())
            params.Jp     = float(self.entries["Jp"].get())
            params.Jr     = float(self.entries["Jr"].get())
            params.L      = float(self.entries["L"].get())
            params.delta1 = float(self.entries["delta1"].get())

            omega_min  = float(self.entries["omega_min"].get())
            omega_max  = float(self.entries["omega_max"].get())
            num_points = int(self.entries["num_points"].get())
            hatch_step = int(self.entries["hatch_step"].get())

            if omega_min >= omega_max:
                raise ValueError("ω мин должно быть меньше ω макс")
            if num_points < 10:
                raise ValueError("Число точек должно быть не меньше 10")
            if hatch_step < 1:
                raise ValueError("Шаг штриховки должен быть ≥ 1")

            return {
                "params": params,
                "omega_min": omega_min,
                "omega_max": omega_max,
                "num_points": num_points,
                "hatch_step": hatch_step,
            }
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Проверьте параметры:\n{e}")
            return None

    # ========== D-кривая со штриховкой ==========

    def add_d_curve(self):
        """Добавить ещё одну D-кривую к графику (для сравнения разных L)."""
        cfg = self._read_params()
        if cfg is None:
            return

        # Определяем размер штриха адаптивно — 3% от диапазона по X
        # Сначала строим без штриховки, чтобы оценить диапазон
        try:
            preview = borshtanga_core.build_d_curve(
                cfg["params"], cfg["omega_min"], cfg["omega_max"], 500
            )
        except Exception as e:
            messagebox.showerror("Ошибка расчёта", str(e))
            return

        if not preview:
            messagebox.showerror("Ошибка", "Кривая получилась пустой")
            return

        re_vals = [p[0] for p in preview]
        im_vals = [p[1] for p in preview]
        x_range = max(re_vals) - min(re_vals)
        y_range = max(im_vals) - min(im_vals)
        hatch_length = 0.03 * max(x_range, y_range)

        # Теперь полный расчёт со штриховкой
        try:
            points = borshtanga_core.build_d_curve_with_hatching(
                cfg["params"],
                cfg["omega_min"],
                cfg["omega_max"],
                cfg["num_points"],
                hatch_length,
                cfg["hatch_step"],
            )
        except Exception as e:
            messagebox.showerror("Ошибка расчёта", str(e))
            return

        # Сохраняем и перерисовываем все кривые
        self.curves.append({
            "L": cfg["params"].L,
            "delta1": cfg["params"].delta1,
            "points": points,
        })
        self._redraw_dcurves()

    def _redraw_dcurves(self):
        """Перерисовывает все накопленные кривые на вкладке D-разбиения."""
        self._setup_dcurve_axes()

        colors = ["blue", "red", "green", "purple", "orange", "brown"]

        for idx, curve_data in enumerate(self.curves):
            color = colors[idx % len(colors)]
            points = curve_data["points"]

            re_vals = [p.re for p in points]
            im_vals = [p.im for p in points]

            # Сама кривая
            self.ax_d.plot(
                re_vals, im_vals,
                color=color, linewidth=1.0,
                label=f"L = {curve_data['L']} м, δ₁ = {curve_data['delta1']:.1e}"
            )

            # Штриховка: для точек с ненулевым hatch_dx/dy рисуем короткие отрезки
            for p in points:
                if p.hatch_dx != 0.0 or p.hatch_dy != 0.0:
                    self.ax_d.plot(
                        [p.re, p.re + p.hatch_dx],
                        [p.im, p.im + p.hatch_dy],
                        color=color, linewidth=0.7, alpha=0.8
                    )

        if self.curves:
            self.ax_d.legend(loc="upper right", fontsize=9)

        self.canvas_d.draw()

    def clear_curves(self):
        """Очистить все кривые."""
        self.curves = []
        self._redraw_dcurves()


    # ========== Диаграмма устойчивости ==========

    def plot_stability_diagram(self):
        cfg = self._read_params()
        if cfg is None:
            return

        # Длины L из Рис. 3 отчёта
        L_values = [2.5, 3.0, 4.0, 5.0, 6.0]

        # Диапазон δ₁ — равномерно от ~0.3e-5 до 3.5e-5 (как на оси Y)
        delta1_values = []
        d1 = 0.3e-5
        while d1 <= 3.5e-5 + 1e-12:
            delta1_values.append(d1)
            d1 += 0.2e-5

        self._setup_stability_axes()
        colors = ["blue", "green", "red", "cyan", "magenta"]
        markers = ["o", "s", "^", "D", "v"]

        base = cfg["params"]
        # Расширяем диапазон ω для надёжного поиска пересечений
        omega_min = 0.1
        omega_max = max(abs(cfg["omega_min"]), abs(cfg["omega_max"]))
        num_search = 10000  # много точек для точного поиска корней

        any_curve_drawn = False

        for li, L in enumerate(L_values):
            xs, ys = [], []
            for d1 in delta1_values:
                p = borshtanga_core.BorshtangaParams()
                p.G = base.G
                p.rho = base.rho
                p.Jp = base.Jp
                p.Jr = base.Jr
                p.L = L
                p.delta1 = d1

                crossings = self._find_real_axis_crossings(
                    p, omega_min, omega_max, num_search
                )
                for re_cross in crossings:
                    xs.append(re_cross)
                    ys.append(d1)

            if xs:
                self.ax_s.plot(
                    xs, ys,
                    marker=markers[li % len(markers)],
                    linestyle="--",
                    color=colors[li % len(colors)],
                    label=f"L = {L} м",
                    markersize=5,
                    linewidth=0.8,
                )
                any_curve_drawn = True

        if any_curve_drawn:
            self.ax_s.legend(loc="upper right")
        else:
            messagebox.showwarning(
                "Нет пересечений",
                "Не найдено пересечений D-кривой с действительной осью.\n"
                "Попробуйте увеличить диапазон ω или число точек."
            )

        self.ax_s.set_title("Диаграмма устойчивости")
        self.canvas_s.draw()
        self.notebook.select(self.tab_stability)

    def _find_real_axis_crossings(self, params, omega_min, omega_max, num):
        step = (omega_max - omega_min) / (num - 1)

        prev_im = None
        prev_re = None
        crossings = []

        for i in range(num):
            omega = omega_min + i * step
            d = borshtanga_core.compute_delta_hat(params, omega)

            if prev_im is not None and prev_im * d.imag < 0:
                # Линейная интерполяция точки, где Im меняет знак
                t = -prev_im / (d.imag - prev_im)
                re_cross = prev_re + t * (d.real - prev_re)
                # Берём только левую полуплоскость (как на Рис. 3)
                if re_cross < 0:
                    crossings.append(re_cross)

            prev_im = d.imag
            prev_re = d.real

        return crossings

    # ========== Сохранение ==========

    def save_current_plot(self):
        """Сохраняет график активной вкладки в файл."""
        active = self.notebook.index(self.notebook.select())
        if active == 0:
            fig = self.fig_d
            default_name = "d_curve.png"
        else:
            fig = self.fig_s
            default_name = "stability_diagram.png"

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[
                ("PNG", "*.png"),
                ("PDF", "*.pdf"),
                ("SVG", "*.svg"),
                ("Все файлы", "*.*"),
            ]
        )
        if path:
            try:
                fig.savefig(path, dpi=200, bbox_inches="tight")
                messagebox.showinfo("Сохранено", f"График сохранён:\n{path}")
            except Exception as e:
                messagebox.showerror("Ошибка сохранения", str(e))


def main():
    root = tk.Tk()
    app = BorshtangaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()