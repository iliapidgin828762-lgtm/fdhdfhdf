import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("800x600")

        # Загрузка данных
        self.trainings = self.load_data()

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # Форма ввода
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку")
        input_frame.pack(fill="x", padx=10, pady=5)

        # Дата
        ttk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Тип тренировки
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.type_entry = ttk.Combobox(input_frame, values=[
            "Бег", "Плавание", "Велоспорт", "Силовая", "Йога", "Кроссфит"
        ])
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        # Длительность
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(input_frame)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        ttk.Button(input_frame, text="Добавить тренировку", command=self.add_training).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Фильтры
        filter_frame = ttk.LabelFrame(self.root, text="Фильтры")
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Тип:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.filter_type = ttk.Combobox(filter_frame, values=["Все"] + [
            "Бег", "Плавание", "Велоспорт", "Силовая", "Йога", "Кроссфит"
        ])
        self.filter_type.set("Все")
        self.filter_type.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Дата:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.filter_date = ttk.Entry(filter_frame)
        self.filter_date.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(filter_frame, text="Применить фильтры", command=self.apply_filters).grid(
            row=0, column=4, padx=5, pady=5
        )

        # Таблица
        columns = ("ID", "Дата", "Тип", "Длительность (мин)")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

    def validate_input(self):
        # Проверка даты
        try:
            date_obj = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD")
            return False

        # Проверка длительности
        try:
            duration = float(self.duration_entry.get())
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом")
            return False

        return True

    def add_training(self):
        if not self.validate_input():
            return

        training = {
            "id": len(self.trainings) + 1,
            "date": self.date_entry.get(),
            "type": self.type_entry.get(),
            "duration": float(self.duration_entry.get())
        }

        self.trainings.append(training)
        self.save_data()
        self.refresh_table()
        self.clear_form()

    def clear_form(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.set("")
        self.duration_entry.delete(0, tk.END)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtered_trainings = self.apply_current_filters()
        for training in filtered_trainings:
            self.tree.insert("", "end", values=(
                training["id"],
                training["date"],
                training["type"],
                training["duration"]
            ))

    def apply_filters(self):
        self.refresh_table()

    def apply_current_filters(self):
        filtered = self.trainings

        # Фильтр по типу
        selected_type = self.filter_type.get()
        if selected_type != "Все":
            filtered = [t for t in filtered if t["type"] == selected_type]

        # Фильтр по дате
        date_filter = self.filter_date.get()
        if date_filter:
            filtered = [t for t in filtered if date_filter in t["date"]]

        return filtered

    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=2)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
