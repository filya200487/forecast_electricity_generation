import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


# Функция для загрузки данных из файла и отображения графика
def load_and_forecast():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("XLSX files", "*.xlsx")])
    if file_path:
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise Exception("Неподдерживаемый формат файла")

            df['ds'] = pd.to_datetime(df['year'], format='%Y')
            df['y'] = df['electricity_generation']

            # Здесь создайте модель Prophet и выполните прогноз
            model = Prophet()
            model.fit(df)

            # Запросите у пользователя количество лет для прогноза
            years_to_forecast = simpledialog.askinteger("Введите количество лет для прогноза", "Количество лет:")
            if years_to_forecast is not None:
                future = model.make_future_dataframe(periods=years_to_forecast*365, freq='D')
                forecast = model.predict(future)

                # Создаем новое окно Tkinter для отображения графика
                result_window = tk.Toplevel(root)
                result_window.title("График прогноза потребления энергии")

                # Отобразите график прогноза в окне Tkinter
                fig = model.plot(forecast, ax=plt.gca())
                plt.title("Прогноз потребления энергии")
                plt.tight_layout()
                plt.grid(True)

                # Вставляем график в Tkinter окно
                canvas = FigureCanvasTkAgg(fig, master=result_window)
                canvas.get_tk_widget().pack()
                canvas.draw()

        except Exception as e:
            tk.messagebox.showerror("Ошибка", str(e))


# Создаем окно Tkinter
root = tk.Tk()
root.title("Прогноз потребления энергии")

# Создаем кнопку для загрузки файла и выполнения прогноза
load_button = tk.Button(root, text="Загрузить файл и выполнить прогноз", command=load_and_forecast)
load_button.pack()

# Запускаем главный цикл Tkinter
root.mainloop()
