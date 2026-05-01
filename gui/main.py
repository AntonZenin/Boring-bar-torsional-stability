import tkinter as tk
from tkinter import ttk, messagebox
import borshtanga_core  

# Подключаем matplotlib для встраивания графиков прямо в окно Tkinter
import matplotlib
matplotlib.use("TkAgg")  # бэкенд для работы с Tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class BorshtangaApp:
    """Класс главного окна приложения."""

    def __init__(self, root):
        self.root = root
        self.root.title("Устойчивость расточной борштанги — D-разбиение")
        self.root.geometry("1100x700")

        # Создаём интерфейс
        self._create_widgets()

    def _create_widgets(self):
        """Создаёт все элементы интерфейса."""

        # Главный контейнер: слева — параметры, справа — график
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ===== ЛЕВАЯ ПАНЕЛЬ: ввод параметров =====
        params_frame = ttk.LabelFrame(main_frame, text="Параметры системы", padding=10)
        params_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Словарь полей ввода: имя → (Entry виджет, значение по умолчанию, описание)
        # Стандартные значения для стальной борштанги
        self.param_specs = [
            ("G",      "8.1e10",  "Модуль сдвига G, Па"),
            ("rho",    "7850",    "Плотность ρ, кг/м³"),
            ("Jp",     "1.0e-7",  "Полярный момент инерции Jₚ, м⁴"),
            ("Jr",     "0.01",    "Момент инерции головки Jᵣ, кг·м²"),
            ("L",      "2.5",     "Длина борштанги L, м"),
            ("delta1", "1.0e-5",  "Коэффициент трения δ₁"),
        ]

        self.entries = {}  # сюда сохраним ссылки на виджеты ввода

        for i, (name, default, label) in enumerate(self.param_specs):
            ttk.Label(params_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(params_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.entries[name] = entry

        # Параметры построения кривой
        ttk.Separator(params_frame, orient=tk.HORIZONTAL).grid(
            row=len(self.param_specs), column=0, columnspan=2, sticky=tk.EW, pady=10
        )

        ttk.Label(params_frame, text="Параметры расчёта:", font=("", 9, "bold")).grid(
            row=len(self.param_specs) + 1, column=0, columnspan=2, sticky=tk.W
        )

        self.curve_specs = [
            ("omega_min", "-1000", "ω мин"),
            ("omega_max",  "1000", "ω макс"),
            ("num_points", "5000", "Число точек"),
        ]

        for i, (name, default, label) in enumerate(self.curve_specs):
            row = len(self.param_specs) + 2 + i
            ttk.Label(params_frame, text=label).grid(row=row, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(params_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=row, column=1, padx=5, pady=3)
            self.entries[name] = entry

        # Кнопка построения
        plot_btn = ttk.Button(
            params_frame,
            text="Построить кривую D-разбиения",
            command=self.plot_d_curve
        )
        plot_btn.grid(
            row=len(self.param_specs) + 2 + len(self.curve_specs),
            column=0, columnspan=2, pady=15, sticky=tk.EW
        )

        # ===== ПРАВАЯ ПАНЕЛЬ: график =====
        plot_frame = ttk.LabelFrame(main_frame, text="Кривая D-разбиения", padding=5)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Создаём фигуру matplotlib
        self.figure = Figure(figsize=(7, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self._setup_axes()

        # Встраиваем matplotlib canvas в Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Панель навигации matplotlib (zoom, сохранение и т.д.)
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()

    def _setup_axes(self):
        """Настройка осей графика — стиль как на Рис. 4."""
        self.ax.clear()
        self.ax.set_title("Кривая D-разбиения")
        self.ax.set_xlabel(r"$\mathrm{Re}\,\hat{\delta}$")
        self.ax.set_ylabel(r"$\mathrm{Im}\,\hat{\delta}$")
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.ax.axhline(0, color="black", linewidth=0.5)
        self.ax.axvline(0, color="black", linewidth=0.5)

    def _read_params(self):
        """Считывает параметры из полей ввода и возвращает объект BorshtangaParams.
        Если ввод некорректен — выбрасывает исключение."""
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

            if omega_min >= omega_max:
                raise ValueError("ω мин должно быть меньше ω макс")
            if num_points < 10:
                raise ValueError("Число точек должно быть не меньше 10")

            return params, omega_min, omega_max, num_points

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Проверьте параметры:\n{e}")
            return None

    def plot_d_curve(self):
        """Обработчик кнопки: строит кривую D-разбиения."""
        result = self._read_params()
        if result is None:
            return
        params, omega_min, omega_max, num_points = result

        # Вызываем C++ функцию для построения кривой
        try:
            curve = borshtanga_core.build_d_curve(params, omega_min, omega_max, num_points)
        except Exception as e:
            messagebox.showerror("Ошибка расчёта", f"Не удалось построить кривую:\n{e}")
            return

        # Разделяем на массивы X (Re) и Y (Im)
        re_parts = [point[0] for point in curve]
        im_parts = [point[1] for point in curve]

        # Перерисовываем график
        self._setup_axes()
        self.ax.plot(re_parts, im_parts, color="blue", linewidth=1.0,
                     label=f"L = {params.L} м")
        self.ax.legend(loc="upper right")
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = BorshtangaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()