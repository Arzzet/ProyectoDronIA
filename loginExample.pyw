import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
from ttkthemes import ThemedTk

from tkinter import messagebox


import sqlite3

def init_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    # Add a sample user (admin) with a hashed password (password)
    # In practice, use a proper password hashing library, such as bcrypt or Argon2
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password_hash)
        VALUES (?, ?)
    """, ("admin", "5f4dcc3b5aa765d61d8327deb882cf99"))

    connection.commit()
    connection.close()

import hashlib

def login():
    username = username_entry.get()
    password = password_entry.get()

    password_hash = hashlib.md5(password.encode()).hexdigest()

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    user = cursor.fetchone()
    connection.close()

    if user:
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        create_main_menu()
    else:
        messagebox.showerror("Error", "Incorrect username or password")



def create_login_window():
    global login_window, username_entry, password_entry

    login_window = ThemedTk(theme="arc")
    login_window.title("Login")

    login_window.configure(bg="#3a3a3a")
    login_window.geometry("300x150")

    label_font = Font(family="Helvetica", size=12, weight="bold")
    entry_font = Font(family="Helvetica", size=11)
    button_font = Font(family="Helvetica", size=11, weight="bold")

    style = ttk.Style()
    style.configure("TLabel", background="#3a3a3a", foreground="#ffffff", font=label_font)
    style.configure("TEntry", font=entry_font)
    style.configure("TButton", font=button_font)

    ttk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=(20, 5))
    username_entry = ttk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=(20, 5))

    ttk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Button(login_window, text="Login", command=login).grid(row=2, column=1, padx=10, pady=10)

    login_window.mainloop()


def create_main_menu():
    main_menu = ThemedTk(theme="arc")
    main_menu.title("Main Menu")

    main_menu.configure(bg="#3a3a3a")
    main_menu.geometry("300x200")

    button_font = Font(family="Helvetica", size=11, weight="bold")

    style = ttk.Style()
    style.configure("TButton", font=button_font)

    ttk.Button(main_menu, text="Option 1", width=20).grid(row=0, column=0, padx=10, pady=(30, 10))
    ttk.Button(main_menu, text="Option 2", width=20).grid(row=1, column=0, padx=10, pady=10)
    ttk.Button(main_menu, text="Option 3", width=20).grid(row=2, column=0, padx=10, pady=10)

    main_menu.mainloop()


if __name__ == "__main__":
    init_database()
    create_login_window()
