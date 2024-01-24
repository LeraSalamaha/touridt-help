import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import psycopg2
from config import host, user, password, db_name


class TouristGuide:
    def __init__(self):
        # Создаем окно
        self.window = tk.Tk()
        self.window.geometry("900x600")
        self.window.configure(bg="seagreen")
        self.window.title("Справочник туриста")

        # Устанавливаем заголовок окна
        self.label = tk.Label(self.window, text="Справочник туриста", background="seagreen", font=("waree", 45))
        self.label.pack()

        # Подключаемся к базе данных
        self.conn = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        self.cursor = self.conn.cursor()

        # Получаем список стран из базы данных
        self.cursor.execute("SELECT name_country FROM country")
        self.countries = self.cursor.fetchall()

        # Создаем метку с текстом
        self.country_label = tk.Label(self.window, text="Страна:", background="seagreen", font=("waree", 15))
        self.country_label.pack()

        # Создаем Combobox для выбора страны
        self.selected_country = tk.StringVar()
        self.combobox_country = ttk.Combobox(self.window, textvariable=self.selected_country)
        self.combobox_country['values'] = self.countries
        self.combobox_country.pack()

        # Создаем метку с текстом
        self.city_label = tk.Label(self.window, text="Город:", background="seagreen", font=("waree", 15))
        self.city_label.pack()

        # Создаем Combobox для выбора города
        self.selected_city = tk.StringVar()
        self.combobox_city = ttk.Combobox(self.window, textvariable=self.selected_city)
        self.combobox_city.pack()

        # Создаем метку с текстом
        self.tour_label = tk.Label(self.window, text="Тур:", background="seagreen", font=("waree", 15))
        self.tour_label.pack()

        # Создаем Combobox для выбора тура
        self.selected_tour = tk.StringVar()
        self.combobox_tour = ttk.Combobox(self.window, textvariable=self.selected_tour)
        self.combobox_tour.pack()

        # Создаем метку с текстом
        self.voucher_label = tk.Label(self.window, text="Путевка:", background="seagreen", font=("waree", 15))
        self.voucher_label.pack()

        # Создаем виджет ScrolledText
        self.text_area = scrolledtext.ScrolledText(self.window, width=70, height=15)
        self.text_area.configure(background="mediumseagreen")
        self.text_area.pack()

        # Привязываем функции обновления списков городов и туров к соответствующим событиям выбора
        self.combobox_country.bind("<<ComboboxSelected>>", self.update_cities)
        self.combobox_city.bind("<<ComboboxSelected>>", self.update_tours)
        self.combobox_tour.bind("<<ComboboxSelected>>", self.display_voucher)

        # Запускаем главный цикл обработки событий
        self.window.mainloop()

    def update_cities(self, event):
        selected_country = self.combobox_country.get()
        self.cursor.execute("""
            SELECT name_city
            FROM city
            WHERE country_id = (
                SELECT country_id
                FROM country
                WHERE name_country = %s
            )
        """, (selected_country,))
        cities = self.cursor.fetchall()
        self.combobox_city['values'] = [city[0] for city in cities]

    def update_tours(self, event):
        selected_city_id = self.combobox_city.current() + 1
        self.cursor.execute(
            "SELECT tour.name_tour, tour.tour_id FROM tour INNER JOIN city ON tour.city_id = city.city_id WHERE city.city_id=%s",
            (selected_city_id,))
        tours = self.cursor.fetchall()
        self.combobox_tour['values'] = [tour[0] for tour in tours]

    def display_voucher(self, event):
        selected_tour_id = self.combobox_tour.current() + 1
        self.cursor.execute("SELECT * FROM voucher WHERE tour_id=%s", (selected_tour_id,))
        vouchers = self.cursor.fetchall()
        self.text_area.delete(1.0, tk.END)  # Очищаем содержимое ScrolledText
        for voucher in vouchers:
            voucher_id, tour_id, num_day, meal, hotel, road, excursion, type_tour, price, date_tour = voucher
            self.text_area.insert(tk.END, f"Длительность: {num_day} дней\n")
            self.text_area.insert(tk.END, f"Питание: {meal}\n")
            self.text_area.insert(tk.END, f"Отель: {hotel}\n")
            self.text_area.insert(tk.END, f"Транспорт: {road}\n")
            self.text_area.insert(tk.END, f"Экскурсии: {excursion}\n")
            self.text_area.insert(tk.END, f"Тип тура: {type_tour}\n")
            self.text_area.insert(tk.END, f"Цена: {price} руб.\n")
            self.text_area.insert(tk.END, f"Дата тура: {date_tour}\n")
            self.text_area.insert(tk.END, "-" * 20 + "\n")

# Создаем экземпляр класса TouristGuide и запускаем программу
tourist_guide = TouristGuide()