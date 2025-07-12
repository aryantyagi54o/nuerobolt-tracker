import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from PIL import Image, ImageTk

# ===== Database Setup =====
conn = sqlite3.connect("aiml_tracker.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        question_name TEXT,
        topic TEXT,
        status TEXT,
        remarks TEXT,
        mock_test INTEGER,
        revision_done INTEGER
    )
''')
conn.commit()

# ===== Save Function =====
def save_entry():
    date_val = date_entry.get()
    name_val = name_entry.get()
    topic_val = topic_entry.get()
    status_val = status_entry.get()
    remarks_val = remarks_entry.get()
    mock_val = 1 if mock_var.get() else 0
    revision_val = 1 if revision_var.get() else 0

    if not (date_val and name_val and topic_val and status_val):
        messagebox.showwarning("Incomplete", "Please fill all required fields")
        return

    cursor.execute('''
        INSERT INTO progress (date, question_name, topic, status, remarks, mock_test, revision_done)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date_val, name_val, topic_val, status_val, remarks_val, mock_val, revision_val))
    conn.commit()
    messagebox.showinfo("Success", "Progress saved successfully")
    clear_fields()
    update_treeview()

# ===== Clear Fields =====
def clear_fields():
    name_entry.delete(0, tk.END)
    topic_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)
    remarks_entry.delete(0, tk.END)
    mock_var.set(False)
    revision_var.set(False)

# ===== Load Data =====
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT date, question_name, topic, status, remarks, mock_test, revision_done FROM progress ORDER BY id DESC")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=(
            row[0], row[1], row[2], row[3], row[4],
            "Yes" if row[5] else "No",
            "Yes" if row[6] else "No"
        ))

# ===== GUI Setup =====
root = tk.Tk()
root.title("NeuroBolt Coding Tracker")
root.geometry("950x620")
root.configure(bg="#00b894")  # turquoise background

# ===== Outer Frame =====
container = tk.Frame(root, bg="#dfe6e9", bd=2, relief=tk.RIDGE)
container.place(relx=0.5, rely=0.5, anchor="center", width=900, height=580)

# ===== Heading =====
tk.Label(container, text="NeuroBolt Coding Tracker", bg="#dfe6e9",
         fg="#2d3436", font=("Helvetica", 22, "bold")).pack(pady=10)

# ===== Input Form =====
form_frame = tk.Frame(container, bg="#dfe6e9")
form_frame.pack(pady=10)

label_opts = {"bg": "#dfe6e9", "fg": "#2d3436", "font": ("Arial", 10, "bold")}
entry_opts = {"width": 40}

tk.Label(form_frame, text="Date (YYYY-MM-DD):", **label_opts).grid(row=0, column=0, sticky="e", padx=5, pady=4)
date_entry = tk.Entry(form_frame, **entry_opts)
date_entry.insert(0, date.today().isoformat())
date_entry.grid(row=0, column=1, pady=4)

tk.Label(form_frame, text="Question Name:", **label_opts).grid(row=1, column=0, sticky="e", padx=5)
name_entry = tk.Entry(form_frame, **entry_opts)
name_entry.grid(row=1, column=1, pady=4)

tk.Label(form_frame, text="Topic:", **label_opts).grid(row=2, column=0, sticky="e", padx=5)
topic_entry = tk.Entry(form_frame, **entry_opts)
topic_entry.grid(row=2, column=1, pady=4)

tk.Label(form_frame, text="Status (✅/⏳/❌):", **label_opts).grid(row=3, column=0, sticky="e", padx=5)
status_entry = tk.Entry(form_frame, **entry_opts)
status_entry.grid(row=3, column=1, pady=4)

tk.Label(form_frame, text="Remarks:", **label_opts).grid(row=4, column=0, sticky="e", padx=5)
remarks_entry = tk.Entry(form_frame, **entry_opts)
remarks_entry.grid(row=4, column=1, pady=4)

mock_var = tk.BooleanVar()
revision_var = tk.BooleanVar()

tk.Checkbutton(form_frame, text="Mock Test Done", variable=mock_var, bg="#dfe6e9").grid(row=5, column=0, pady=4)
tk.Checkbutton(form_frame, text="Revision Done", variable=revision_var, bg="#dfe6e9").grid(row=5, column=1, pady=4)

# ===== Save Button =====
tk.Button(container, text="💾 Save Progress", command=save_entry,
          bg="#0984e3", fg="white", font=("Arial", 11, "bold"), padx=10, pady=4).pack(pady=8)

# ===== Treeview =====
tree = ttk.Treeview(container, columns=("Date", "Question", "Topic", "Status", "Remarks", "Mock", "Revision"), show="headings")
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
style.configure("Treeview", font=("Arial", 10), rowheight=24)

for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# ===== Footer =====
tk.Label(container, text="Built by Aryan — NeuroBolt Tracker", bg="#dfe6e9", fg="gray").pack(pady=5)

# ===== Run GUI =====
update_treeview()
root.mainloop()
conn.close()
