import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")
        
        # История паролей
        self.history = []
        self.load_history()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Длина пароля
        length_frame = ttk.Frame(self.root)
        length_frame.pack(pady=10, fill="x", padx=20)
        ttk.Label(length_frame, text="Длина пароля:").pack(side="left")
        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(
            length_frame,
            from_=4, to=64,
            variable=self.length_var,
            orient="horizontal"
        )
        self.length_scale.pack(side="left", fill="x", expand=True, padx=10)
        self.length_label = ttk.Label(length_frame, text="12")
        self.length_label.pack(side="left")
        self.length_scale.config(command=self.update_length_display)
        
        # Опции символов
        options_frame = ttk.LabelFrame(self.root, text="Типы символов")
        options_frame.pack(pady=10, fill="x", padx=20)
        
        self.use_letters = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Буквы (a‑z, A‑Z)", variable=self.use_letters).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Цифры (0‑9)", variable=self.use_digits).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Спецсимволы (!@#$%)", variable=self.use_special).pack(anchor="w")
        
        # Кнопка генерации
        generate_btn = ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password)
        generate_btn.pack(pady=10)
        
        # Поле вывода пароля
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(self.root, textvariable=self.password_var, font=("Courier", 12), justify="center")
        password_entry.pack(pady=5, fill="x", padx=20)
        
        # Таблица истории
        history_frame = ttk.LabelFrame(self.root, text="История паролей")
        history_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        columns = ("№", "Пароль", "Длина", "Типы символов")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        self.history_tree.pack(fill="both", expand=True)
        
        # Кнопки очистки истории
        clear_btn = ttk.Button(history_frame, text="Очистить историю", command=self.clear_history)
        clear_btn.pack(pady=5)
    
    def update_length_display(self, value):
        self.length_label.config(text=str(int(float(value))))
    
    def generate_password(self):
        length = self.length_var.get()
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа")
            return
        if length > 64:
            messagebox.showerror("Ошибка", "Максимальная длина пароля — 64 символа")
            return
        
        chars = ""
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_digits.get():
            chars += string.digits
        if self.use_special.get():
            chars += "!@#$%^&*"
        
        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return
        
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)
        
        # Добавляем в историю
        char_types = []
        if self.use_letters.get(): char_types.append("Буквы")
        if self.use_digits.get(): char_types.append("Цифры")
        if self.use_special.get(): char_types.append("Спец")
        self.add_to_history(password, length, ", ".join(char_types))
    
    def add_to_history(self, password, length, char_types):
        entry = {
            "password": password,
            "length": length,
            "char_types": char_types
        }
        self.history.append(entry)
        self.update_history_table()
        self.save_history()
    
    def update_history_table(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        for i, entry in enumerate(self.history[-10:], 1):  # Последние 10 записей
            self.history_tree.insert("", "end", values=(i, entry["password"], entry["length"], entry["char_types"]))
    
    def save_history(self):
        with open("password_history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
    
    def load_history(self):
        if os.path.exists("password_history.json"):
            try:
                with open("password_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def clear_history(self):
        self.history = []
        self.update_history_table()
        self.save_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
