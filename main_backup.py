import tkinter as tk
from tkinter import messagebox

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Student Management System")
root.geometry("1000x650")
root.resizable(False, False)

# ---------------- COLORS ----------------
BG_COLOR = "#f4f6f8"
HEADER_COLOR = "#1e3a8a"
BUTTON_COLOR = "#2563eb"

root.configure(bg=BG_COLOR)

# ---------------- HEADER ----------------
header = tk.Frame(root, bg=HEADER_COLOR, height=100)
header.pack(fill="x")

title = tk.Label(
    header,
    text="Student Management System",
    font=("Arial", 26, "bold"),
    bg=HEADER_COLOR,
    fg="white"
)
title.pack(pady=30)

# ---------------- WELCOME ----------------
welcome = tk.Label(
    root,
    text="Welcome to Student Management System",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg="#222222"
)
welcome.pack(pady=50)


# ---------------- BUTTON FUNCTION ----------------
def start_application():
    messagebox.showinfo(
        "Student Management System",
        "Application Started Successfully!"
    )


# ---------------- START BUTTON ----------------
start_button = tk.Button(
    root,
    text="START APPLICATION",
    font=("Arial", 15, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    padx=30,
    pady=12,
    cursor="hand2",
    command=start_application
)
start_button.pack()


# ---------------- FOOTER ----------------
footer = tk.Label(
    root,
    text="Student Management System © 2026",
    font=("Arial", 10),
    bg=BG_COLOR,
    fg="gray"
)
footer.pack(side="bottom", pady=20)

# ---------------- RUN APP ----------------
root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL UNIQUE,
    course TEXT NOT NULL,
    year TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
""")

conn.commit()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Student Management System")
root.geometry("1100x700")
root.resizable(False, False)
root.configure(bg="#f4f6f8")


# =========================================================
# COLORS
# =========================================================

HEADER_COLOR = "#1e3a8a"
BUTTON_COLOR = "#2563eb"
GREEN_COLOR = "#16a34a"
RED_COLOR = "#dc2626"
ORANGE_COLOR = "#ea580c"
BG_COLOR = "#f4f6f8"


# =========================================================
# FUNCTIONS
# =========================================================

def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    year_combo.set("")
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

    selected_id.set("")


def add_student():

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    course = course_entry.get().strip()
    year = year_combo.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "" or roll == "" or course == "" or year == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill all required fields."
        )
        return

    try:

        cursor.execute("""
        INSERT INTO students
        (name, roll_no, course, year, phone, email)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, roll, course, year, phone, email))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Roll Number already exists."
        )


def display_students():

    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute("""
    SELECT id, name, roll_no, course, year, phone, email
    FROM students
    ORDER BY id DESC
    """)

    records = cursor.fetchall()

    for record in records:
        student_table.insert("", tk.END, values=record)


def select_student(event):

    selected = student_table.focus()

    if not selected:
        return

    values = student_table.item(selected, "values")

    if not values:
        return

    selected_id.set(values[0])

    clear_all_entries_without_id()

    name_entry.insert(0, values[1])
    roll_entry.insert(0, values[2])
    course_entry.insert(0, values[3])
    year_combo.set(values[4])
    phone_entry.insert(0, values[5])
    email_entry.insert(0, values[6])


def clear_all_entries_without_id():

    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    year_combo.set("")
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


def update_student():

    student_id = selected_id.get()

    if student_id == "":
        messagebox.showwarning(
            "Select Student",
            "Please select a student from the table."
        )
        return

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    course = course_entry.get().strip()
    year = year_combo.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "" or roll == "" or course == "" or year == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill all required fields."
        )
        return

    try:

        cursor.execute("""
        UPDATE students
        SET name=?,
            roll_no=?,
            course=?,
            year=?,
            phone=?,
            email=?
        WHERE id=?
        """, (
            name,
            roll,
            course,
            year,
            phone,
            email,
            student_id
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Roll Number already exists."
        )


def delete_student():

    student_id = selected_id.get()

    if student_id == "":
        messagebox.showwarning(
            "Select Student",
            "Please select a student from the table."
        )
        return

    confirm = messagebox.askyesno(
        "Delete Student",
        "Are you sure you want to delete this student?"
    )

    if confirm:

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Deleted",
            "Student deleted successfully!"
        )

        clear_fields()
        display_students()


def search_student():

    search_text = search_entry.get().strip()

    for item in student_table.get_children():
        student_table.delete(item)

    if search_text == "":
        display_students()
        return

    cursor.execute("""
    SELECT id, name, roll_no, course, year, phone, email
    FROM students
    WHERE name LIKE ?
       OR roll_no LIKE ?
       OR course LIKE ?
    ORDER BY id DESC
    """, (
        "%" + search_text + "%",
        "%" + search_text + "%",
        "%" + search_text + "%"
    ))

    records = cursor.fetchall()

    for record in records:
        student_table.insert("", tk.END, values=record)


def exit_application():

    confirm = messagebox.askyesno(
        "Exit",
        "Do you want to exit the application?"
    )

    if confirm:
        conn.close()
        root.destroy()


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=90
)

header.pack(fill="x")

title = tk.Label(
    header,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 25, "bold"),
    bg=HEADER_COLOR,
    fg="white"
)

title.pack(pady=25)


# =========================================================
# FORM FRAME
# =========================================================

form_frame = tk.LabelFrame(
    root,
    text=" Student Information ",
    font=("Arial", 13, "bold"),
    bg=BG_COLOR,
    padx=20,
    pady=15
)

form_frame.pack(
    fill="x",
    padx=25,
    pady=15
)


# =========================================================
# VARIABLES
# =========================================================

selected_id = tk.StringVar()


# =========================================================
# NAME
# =========================================================

tk.Label(
    form_frame,
    text="Student Name:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=0, column=0, padx=10, pady=8, sticky="w")

name_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

name_entry.grid(row=0, column=1, padx=10, pady=8)


# =========================================================
# ROLL NUMBER
# =========================================================

tk.Label(
    form_frame,
    text="Roll Number:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=0, column=2, padx=10, pady=8, sticky="w")

roll_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

roll_entry.grid(row=0, column=3, padx=10, pady=8)


# =========================================================
# COURSE
# =========================================================

tk.Label(
    form_frame,
    text="Course:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=1, column=0, padx=10, pady=8, sticky="w")

course_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

course_entry.grid(row=1, column=1, padx=10, pady=8)


# =========================================================
# YEAR
# =========================================================

tk.Label(
    form_frame,
    text="Year:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=1, column=2, padx=10, pady=8, sticky="w")

year_combo = ttk.Combobox(
    form_frame,
    values=[
        "First Year",
        "Second Year",
        "Third Year",
        "Final Year"
    ],
    width=26,
    state="readonly",
    font=("Arial", 11)
)

year_combo.grid(row=1, column=3, padx=10, pady=8)


# =========================================================
# PHONE
# =========================================================

tk.Label(
    form_frame,
    text="Phone:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=2, column=0, padx=10, pady=8, sticky="w")

phone_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

phone_entry.grid(row=2, column=1, padx=10, pady=8)


# =========================================================
# EMAIL
# =========================================================

tk.Label(
    form_frame,
    text="Email:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=2, column=2, padx=10, pady=8, sticky="w")

email_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

email_entry.grid(row=2, column=3, padx=10, pady=8)


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

button_frame.pack(pady=5)


# ADD BUTTON

tk.Button(
    button_frame,
    text="ADD STUDENT",
    font=("Arial", 11, "bold"),
    bg=GREEN_COLOR,
    fg="white",
    width=15,
    cursor="hand2",
    command=add_student
).grid(row=0, column=0, padx=5)


# UPDATE BUTTON

tk.Button(
    button_frame,
    text="UPDATE",
    font=("Arial", 11, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    width=15,
    cursor="hand2",
    command=update_student
).grid(row=0, column=1, padx=5)


# DELETE BUTTON

tk.Button(
    button_frame,
    text="DELETE",
    font=("Arial", 11, "bold"),
    bg=RED_COLOR,
    fg="white",
    width=15,
    cursor="hand2",
    command=delete_student
).grid(row=0, column=2, padx=5)


# CLEAR BUTTON

tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 11, "bold"),
    bg=ORANGE_COLOR,
    fg="white",
    width=15,
    cursor="hand2",
    command=clear_fields
).grid(row=0, column=3, padx=5)


# =========================================================
# SEARCH FRAME
# =========================================================

search_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

search_frame.pack(
    fill="x",
    padx=25,
    pady=10
)

tk.Label(
    search_frame,
    text="Search Student:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).pack(side="left", padx=5)

search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Arial", 11)
)

search_entry.pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="SEARCH",
    font=("Arial", 10, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    width=12,
    cursor="hand2",
    command=search_student
).pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="SHOW ALL",
    font=("Arial", 10, "bold"),
    width=12,
    cursor="hand2",
    command=display_students
).pack(side="left", padx=5)


# =========================================================
# TABLE FRAME
# =========================================================

table_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=5
)


# =========================================================
# SCROLLBAR
# =========================================================

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical"
)

scrollbar.pack(
    side="right",
    fill="y"
)


# =========================================================
# STUDENT TABLE
# =========================================================

columns = (
    "ID",
    "Name",
    "Roll No",
    "Course",
    "Year",
    "Phone",
    "Email"
)

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=scrollbar.set,
    height=10
)

scrollbar.config(
    command=student_table.yview
)


# =========================================================
# TABLE HEADINGS
# =========================================================

for column in columns:

    student_table.heading(
        column,
        text=column
    )


# =========================================================
# TABLE WIDTHS
# =========================================================

student_table.column(
    "ID",
    width=50,
    anchor="center"
)

student_table.column(
    "Name",
    width=170
)

student_table.column(
    "Roll No",
    width=100,
    anchor="center"
)

student_table.column(
    "Course",
    width=130
)

student_table.column(
    "Year",
    width=110
)

student_table.column(
    "Phone",
    width=120
)

student_table.column(
    "Email",
    width=210
)


student_table.pack(
    fill="both",
    expand=True
)


# =========================================================
# SELECT EVENT
# =========================================================

student_table.bind(
    "<ButtonRelease-1>",
    select_student
)


# =========================================================
# EXIT BUTTON
# =========================================================

exit_button = tk.Button(
    root,
    text="EXIT APPLICATION",
    font=("Arial", 11, "bold"),
    bg="#111827",
    fg="white",
    width=20,
    cursor="hand2",
    command=exit_application
)

exit_button.pack(
    pady=10
)


# =========================================================
# LOAD EXISTING STUDENTS
# =========================================================

display_students()


# =========================================================
# RUN APPLICATION
# =========================================================

root.mainloop()



import tkinter as tk
from tkinter import messagebox

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Student Management System")
root.geometry("1000x650")
root.resizable(False, False)

# ---------------- COLORS ----------------
BG_COLOR = "#f4f6f8"
HEADER_COLOR = "#1e3a8a"
BUTTON_COLOR = "#2563eb"

root.configure(bg=BG_COLOR)

# ---------------- HEADER ----------------
header = tk.Frame(root, bg=HEADER_COLOR, height=100)
header.pack(fill="x")

title = tk.Label(
    header,
    text="Student Management System",
    font=("Arial", 26, "bold"),
    bg=HEADER_COLOR,
    fg="white"
)
title.pack(pady=30)

# ---------------- WELCOME ----------------
welcome = tk.Label(
    root,
    text="Welcome to Student Management System",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg="#222222"
)
welcome.pack(pady=50)


# ---------------- BUTTON FUNCTION ----------------
def start_application():
    messagebox.showinfo(
        "Student Management System",
        "Application Started Successfully!"
    )


# ---------------- START BUTTON ----------------
start_button = tk.Button(
    root,
    text="START APPLICATION",
    font=("Arial", 15, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    padx=30,
    pady=12,
    cursor="hand2",
    command=start_application
)
start_button.pack()


# ---------------- FOOTER ----------------
footer = tk.Label(
    root,
    text="Student Management System © 2026",
    font=("Arial", 10),
    bg=BG_COLOR,
    fg="gray"
)
footer.pack(side="bottom", pady=20)

# ---------------- RUN APP ----------------
root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL UNIQUE,
    course TEXT NOT NULL,
    year TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
""")

conn.commit()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Student Management System")
root.geometry("1100x700")
root.resizable(False, False)
root.configure(bg="#f4f6f8")


# =========================================================
# COLORS
# =========================================================

HEADER_COLOR = "#1e3a8a"
BUTTON_COLOR = "#2563eb"
GREEN_COLOR = "#16a34a"
RED_COLOR = "#dc2626"
ORANGE_COLOR = "#ea580c"
BG_COLOR = "#f4f6f8"


# =========================================================
# FUNCTIONS
# =========================================================

def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    year_combo.set("")
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

    selected_id.set("")


def add_student():

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    course = course_entry.get().strip()
    year = year_combo.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "" or roll == "" or course == "" or year == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill all required fields."
        )
        return

    try:

        cursor.execute("""
        INSERT INTO students
        (name, roll_no, course, year, phone, email)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, roll, course, year, phone, email))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Roll Number already exists."
        )


def display_students():

    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute("""
    SELECT id, name, roll_no, course, year, phone, email
    FROM students
    ORDER BY id DESC
    """)

    records = cursor.fetchall()

    for record in records:
        student_table.insert("", tk.END, values=record)


def select_student(event):

    selected = student_table.focus()

    if not selected:
        return

    values = student_table.item(selected, "values")

    if not values:
        return

    selected_id.set(values[0])

    clear_all_entries_without_id()

    name_entry.insert(0, values[1])
    roll_entry.insert(0, values[2])
    course_entry.insert(0, values[3])
    year_combo.set(values[4])
    phone_entry.insert(0, values[5])
    email_entry.insert(0, values[6])


def clear_all_entries_without_id():

    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    year_combo.set("")
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


def update_student():

    student_id = selected_id.get()

    if student_id == "":
        messagebox.showwarning(
            "Select Student",
            "Please select a student from the table."
        )
        return

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    course = course_entry.get().strip()
    year = year_combo.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "" or roll == "" or course == "" or year == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill all required fields."
        )
        return

    try:

        cursor.execute("""
        UPDATE students
        SET name=?,
            roll_no=?,
            course=?,
            year=?,
            phone=?,
            email=?
        WHERE id=?
        """, (
            name,
            roll,
            course,
            year,
            phone,
            email,
            student_id
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Roll Number already exists."
        )


def delete_student():

    student_id = selected_id.get()

    if student_id == "":
        messagebox.showwarning(
            "Select Student",
            "Please select a student from the table."
        )
        return

    confirm = messagebox.askyesno(
        "Delete Student",
        "Are you sure you want to delete this student?"
    )

    if confirm:

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Deleted",
            "Student deleted successfully!"
        )

        clear_fields()
        display_students()


def search_student():

    search_text = search_entry.get().strip()

    for item in student_table.get_children():
        student_table.delete(item)

    if search_text == "":
        display_students()
        return

    cursor.execute("""
    SELECT id, name, roll_no, course, year, phone, email
    FROM students
    WHERE name LIKE ?
       OR roll_no LIKE ?
       OR course LIKE ?
    ORDER BY id DESC
    """, (
        "%" + search_text + "%",
        "%" + search_text + "%",
        "%" + search_text + "%"
    ))

    records = cursor.fetchall()

    for record in records:
        student_table.insert("", tk.END, values=record)


def exit_application():

    confirm = messagebox.askyesno(
        "Exit",
        "Do you want to exit the application?"
    )

    if confirm:
        conn.close()
        root.destroy()


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=90
)

header.pack(fill="x")

title = tk.Label(
    header,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 25, "bold"),
    bg=HEADER_COLOR,
    fg="white"
)

title.pack(pady=25)


# =========================================================
# FORM FRAME
# =========================================================

form_frame = tk.LabelFrame(
    root,
    text=" Student Information ",
    font=("Arial", 13, "bold"),
    bg=BG_COLOR,
    padx=20,
    pady=15
)

form_frame.pack(
    fill="x",
    padx=25,
    pady=15
)


# =========================================================
# VARIABLES
# =========================================================

selected_id = tk.StringVar()


# =========================================================
# NAME
# =========================================================

tk.Label(
    form_frame,
    text="Student Name:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=0, column=0, padx=10, pady=8, sticky="w")

name_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

name_entry.grid(row=0, column=1, padx=10, pady=8)


# =========================================================
# ROLL NUMBER
# =========================================================

tk.Label(
    form_frame,
    text="Roll Number:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=0, column=2, padx=10, pady=8, sticky="w")

roll_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

roll_entry.grid(row=0, column=3, padx=10, pady=8)


# =========================================================
# COURSE
# =========================================================

tk.Label(
    form_frame,
    text="Course:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=1, column=0, padx=10, pady=8, sticky="w")

course_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

course_entry.grid(row=1, column=1, padx=10, pady=8)


# =========================================================
# YEAR
# =========================================================

tk.Label(
    form_frame,
    text="Year:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=1, column=2, padx=10, pady=8, sticky="w")

year_combo = ttk.Combobox(
    form_frame,
    values=[
        "First Year",
        "Second Year",
        "Third Year",
        "Final Year"
    ],
    width=26,
    state="readonly",
    font=("Arial", 11)
)

year_combo.grid(row=1, column=3, padx=10, pady=8)


# =========================================================
# PHONE
# =========================================================

tk.Label(
    form_frame,
    text="Phone:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=2, column=0, padx=10, pady=8, sticky="w")

phone_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

phone_entry.grid(row=2, column=1, padx=10, pady=8)


# =========================================================
# EMAIL
# =========================================================

tk.Label(
    form_frame,
    text="Email:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).grid(row=2, column=2, padx=10, pady=8, sticky="w")

email_entry = tk.Entry(
    form_frame,
    width=28,
    font=("Arial", 11)
)

email_entry.grid(row=2, column=3, padx=10, pady=8)


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

button_frame.pack(pady=5)


# ADD BUTTON

tk.Button(
    button_frame,
    text="ADD STUDENT",
    font=("Arial", 11, "bold"),
    bg=GREEN_COLOR,
    fg="white",
    width=15,
    cursor="hand2",
    command=add_student
).grid(row=0, column=0, padx=5)


# UPDATE BUTTON

tk.Button(
    button_frame,
    text="UPDATE",
    font=("Arial", 11, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    width=15,
    cursor="hand2",
    command=update_student
).grid(row=0, column=1, padx=5)


# DELETE BUTTON

tk.Button(
    button_frame,
    text="DELETE",
    font=("Arial", 11, "bold"),
    bg=RED_COLOR,
    fg="white",
    width=15,
    cursor="hand2",
    command=delete_student
).grid(row=0, column=2, padx=5)


# CLEAR BUTTON

tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 11, "bold"),
    bg=ORANGE_COLOR,
    fg="white",
    width=15,
    cursor="hand2",
    command=clear_fields
).grid(row=0, column=3, padx=5)


# =========================================================
# SEARCH FRAME
# =========================================================

search_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

search_frame.pack(
    fill="x",
    padx=25,
    pady=10
)

tk.Label(
    search_frame,
    text="Search Student:",
    font=("Arial", 11, "bold"),
    bg=BG_COLOR
).pack(side="left", padx=5)

search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Arial", 11)
)

search_entry.pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="SEARCH",
    font=("Arial", 10, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    width=12,
    cursor="hand2",
    command=search_student
).pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="SHOW ALL",
    font=("Arial", 10, "bold"),
    width=12,
    cursor="hand2",
    command=display_students
).pack(side="left", padx=5)


# =========================================================
# TABLE FRAME
# =========================================================

table_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=5
)


# =========================================================
# SCROLLBAR
# =========================================================

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical"
)

scrollbar.pack(
    side="right",
    fill="y"
)


# =========================================================
# STUDENT TABLE
# =========================================================

columns = (
    "ID",
    "Name",
    "Roll No",
    "Course",
    "Year",
    "Phone",
    "Email"
)

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=scrollbar.set,
    height=10
)

scrollbar.config(
    command=student_table.yview
)


# =========================================================
# TABLE HEADINGS
# =========================================================

for column in columns:

    student_table.heading(
        column,
        text=column
    )


# =========================================================
# TABLE WIDTHS
# =========================================================

student_table.column(
    "ID",
    width=50,
    anchor="center"
)

student_table.column(
    "Name",
    width=170
)

student_table.column(
    "Roll No",
    width=100,
    anchor="center"
)

student_table.column(
    "Course",
    width=130
)

student_table.column(
    "Year",
    width=110
)

student_table.column(
    "Phone",
    width=120
)

student_table.column(
    "Email",
    width=210
)


student_table.pack(
    fill="both",
    expand=True
)


# =========================================================
# SELECT EVENT
# =========================================================

student_table.bind(
    "<ButtonRelease-1>",
    select_student
)


# =========================================================
# EXIT BUTTON
# =========================================================

exit_button = tk.Button(
    root,
    text="EXIT APPLICATION",
    font=("Arial", 11, "bold"),
    bg="#111827",
    fg="white",
    width=20,
    cursor="hand2",
    command=exit_application
)

exit_button.pack(
    pady=10
)


# =========================================================
# LOAD EXISTING STUDENTS
# =========================================================

display_students()


# =========================================================
# RUN APPLICATION
# =========================================================

root.mainloop()



