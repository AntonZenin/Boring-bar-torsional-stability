# Исследование устойчивости колебаний расточной борштанги

Программа для математического моделирования динамики расточной борштанги при возбуждении крутильных колебаний. Реализован метод D-разбиения по одному параметру для исследования устойчивости состояния равновесия.

## Архитектура

- **C++ ядро** (`cpp_core/`) — расчёт значений по формуле (10) уравнения кривой D-разбиения
- **Python GUI** (`gui/`) — интерфейс на Tkinter, графики через matplotlib
- **pybind11** — связка между C++ и Python

## Требования

- Python 3.12
- Visual Studio 2022 (C++ Desktop Development)
- CMake 3.15+
- Python-пакеты: `pybind11`, `matplotlib`, `numpy`

## Установка зависимостей

```bash
py -3.12 -m pip install pybind11 matplotlib numpy
```

## Сборка

В корне проекта выполнить:

```bash
.\build.bat
```

После сборки модуль `borshtanga_core.cp312-win_amd64.pyd` появится в папке `gui/`.

## Запуск

```bash
cd gui
py -3.12 main.py
```

## Структура проекта

```
BorshtangaApp/
├── cpp_core/                    # C++ ядро
│   ├── borshtanga_core.hpp      # Заголовок
│   ├── borshtanga_core.cpp      # Реализация формулы (10)
│   └── bindings.cpp             # pybind11 связка
├── gui/                         # Python интерфейс
│   ├── main.py                  # Главное окно
│   └── test_core.py             # Тестовый скрипт C++ ядра
├── CMakeLists.txt               # Конфигурация сборки
├── build.bat                    # Скрипт сборки
└── README.md
```

## Этапы разработки

- [x] Этап 1: C++ ядро с реализацией формулы (10)
- [x] Этап 2: Tkinter GUI с построением кривой D-разбиения
- [ ] Этап 3: Диаграмма устойчивости, штриховка кривой, сохранение графиков

## Теоретическая основа

Уравнение кривой D-разбиения:

$$\hat{\delta} = -p \cdot \lambda_1 \sqrt{1 + \delta_1 p} \cdot \coth\left(\lambda_2 \cdot \frac{p}{\sqrt{1 + \delta_1 p}}\right), \quad p = i\omega$$

где:
- $\lambda_1 = \dfrac{\sqrt{\rho G} \cdot J_p}{J_r}$
- $\lambda_2 = L \cdot \sqrt{\dfrac{\rho}{G}}$
