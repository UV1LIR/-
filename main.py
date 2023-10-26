import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаем соединение с базой данных
conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

# Создаем таблицу для хранения информации о сотрудниках
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        salary REAL NOT NULL
    )
''')
conn.commit()

# Функция для добавления сотрудника
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = float(salary_entry.get())

    cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)", (name, phone, email, salary))
    conn.commit()
    name_entry.delete(0, "end")
    phone_entry.delete(0, "end")
    email_entry.delete(0, "end")
    salary_entry.delete(0, "end")
    load_employees()

# Функция для изменения сотрудника
def edit_employee():
    selected_item = tree.selection()
    if selected_item:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = float(salary_entry.get())
        employee_id = selected_item[0]

        cursor.execute("UPDATE employees SET name = ?, phone = ?, email = ?, salary = ? WHERE id = ?", (name, phone, email, salary, employee_id))
        conn.commit()
        name_entry.delete(0, "end")
        phone_entry.delete(0, "end")
        email.delete(0, "end")
        salary_entry.delete(0, "end")
        load_employees()

# Функция для удаления сотрудника
def delete_employee():
    selected_item = tree.selection()
    if selected_item:
        employee_id = selected_item[0]
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        conn.commit()
        name_entry.delete(0, "end")
        phone_entry.delete(0, "end")
        email_entry.delete(0, "end")
        salary_entry.delete(0, "end")
        load_employees()

# Функция для поиска сотрудника по имени
def search_employee():
    name = search_entry.get()
    cursor.execute("SELECT * FROM employees WHERE name LIKE ?", ('%' + name + '%',))
    employees = cursor.fetchall()
    display_employees(employees)

# Функция для обновления данных в виджете Treeview
def load_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    display_employees(employees)

# Функция для отображения записей в виджете Treeview
def display_employees(employees):
    for record in tree.get_children():
        tree.delete(record)
    for employee in employees:
        tree.insert("", "end", values=employee)

# Создаем графический интерфейс
root = tk.Tk()
root.title("Система управления сотрудниками")

frame = ttk.Frame(root)
frame.pack(pady=10)

# Создаем поля ввода
name_label = ttk.Label(frame, text="ФИО:")
name_label.grid(row=0, column=0)
name_entry = ttk.Entry(frame)
name_entry.grid(row=0, column=1)

phone_label = ttk.Label(frame, text="Номер телефона:")
phone_label.grid(row=1, column=0)
phone_entry = ttk.Entry(frame)
phone_entry.grid(row=1, column=1)

email_label = ttk.Label(frame, text="адрес электронной почты:")
email_label.grid(row=2, column=0)
email_entry = ttk.Entry(frame)
email_entry.grid(row=2, column=1)

salary_label = ttk.Label(frame, text="заработная плата:")
salary_label.grid(row=3, column=0)
salary_entry = ttk.Entry(frame)
salary_entry.grid(row=3, column=1)

add_button = ttk.Button(frame, text="Добавить сотрудника", command=add_employee)
add_button.grid(row=4, column=0, columnspan=2)

edit_button = ttk.Button(frame, text="Изменить сотрудника", command=edit_employee)
edit_button.grid(row=5, column=0, columnspan=2)

delete_button = ttk.Button(frame, text="Удалить сотрудника", command=delete_employee)
delete_button.grid(row=6, column=0, columnspan=2)

# Создаем поле для поиска
search_label = ttk.Label(frame, text="Поиск по имени:")
search_label.grid(row=7, column=0)
search_entry = ttk.Entry(frame)
search_entry.grid(row=7, column=1)
search_button = ttk.Button(frame, text="Найти", command=search_employee)
search_button.grid(row=8, column=0, columnspan=2)

# Создаем виджет Treeview для отображения данных
tree = ttk.Treeview(root, columns=("ID", "Name", "Phone", "EMail", "Salary"))
tree.heading("ID", text="ID")
tree.heading("Name", text="ФИО")
tree.heading("Phone", text="Номер телефона")
tree.heading("EMail", text="адрес электронной почты")
tree.heading("Salary", text="Зарплата")
tree.pack(padx=10, pady=10)

load_employees()

root.mainloop()