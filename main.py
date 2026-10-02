import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime


# =========================================================
# DATABASE
# =========================================================

DB_NAME = "students.db"

conn = sqlite3.connect(DB_NAME)
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")

conn.commit()


# =========================================================
# COLORS
# =========================================================

BG = "#f4f6f9"
SIDEBAR = "#172554"
SIDEBAR_HOVER = "#1e3a8a"
PRIMARY = "#2563eb"
PRIMARY_DARK = "#1d4ed8"
SUCCESS = "#16a34a"
DANGER = "#dc2626"
WARNING = "#ea580c"
PURPLE = "#7c3aed"
WHITE = "#ffffff"
TEXT = "#111827"
MUTED = "#6b7280"
BORDER = "#e5e7eb"


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title("Student Management System")
root.geometry("1250x750")
root.minsize(1100, 680)
root.configure(bg=BG)


# =========================================================
# VARIABLES
# =========================================================

selected_id = None
tree = None

name_var = tk.StringVar()
roll_var = tk.StringVar()
course_var = tk.StringVar()
year_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
search_var = tk.StringVar()

total_students_var = tk.StringVar(value="0")
today_present_var = tk.StringVar(value="0")
total_fees_var = tk.StringVar(value="₹0")
pending_fees_var = tk.StringVar(value="₹0")


# =========================================================
# UTILITY
# =========================================================

def today_date():
    return datetime.now().strftime("%d-%m-%Y")


def clear_fields():

    global selected_id

    selected_id = None

    name_var.set("")
    roll_var.set("")
    course_var.set("")
    year_var.set("")
    phone_var.set("")
    email_var.set("")

    if tree is not None:
        tree.selection_remove(tree.selection())


def update_dashboard_stats():

    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]

    total_students_var.set(str(total))

    today = today_date()

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date=? AND status='Present'
    """, (today,))

    present = cursor.fetchone()[0]

    today_present_var.set(str(present))

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM fees
        WHERE status='Paid'
    """)

    total_fees = cursor.fetchone()[0] or 0

    total_fees_var.set(f"₹{total_fees:,.2f}")

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM fees
        WHERE status='Pending'
    """)

    pending = cursor.fetchone()[0] or 0

    pending_fees_var.set(f"₹{pending:,.2f}")


def display_students(rows=None):

    if tree is None:
        return

    for item in tree.get_children():
        tree.delete(item)

    if rows is None:

        cursor.execute("""
            SELECT
                id,
                name,
                roll_no,
                course,
                year,
                phone,
                email
            FROM students
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

    for row in rows:

        tree.insert(
            "",
            tk.END,
            values=row
        )

    update_dashboard_stats()


# =========================================================
# STUDENT FUNCTIONS
# =========================================================

def add_student():

    name = name_var.get().strip()
    roll = roll_var.get().strip()
    course = course_var.get().strip()
    year = year_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()

    if not name or not roll or not course or not year:

        messagebox.showwarning(
            "Missing Information",
            "Please fill Name, Roll Number, Course and Year."
        )
        return

    try:

        cursor.execute("""
            INSERT INTO students
            (name, roll_no, course, year, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            roll,
            course,
            year,
            phone,
            email
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student added successfully."
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Roll Number already exists."
        )


def select_student(event=None):

    global selected_id

    if tree is None:
        return

    selected = tree.selection()

    if not selected:
        return

    values = tree.item(
        selected[0],
        "values"
    )

    if not values:
        return

    selected_id = int(values[0])

    name_var.set(values[1])
    roll_var.set(values[2])
    course_var.set(values[3])
    year_var.set(values[4])
    phone_var.set(values[5])
    email_var.set(values[6])


def update_student():

    global selected_id

    if selected_id is None:

        messagebox.showwarning(
            "Select Student",
            "Please select a student from the table first."
        )
        return

    name = name_var.get().strip()
    roll = roll_var.get().strip()
    course = course_var.get().strip()
    year = year_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()

    if not name or not roll or not course or not year:

        messagebox.showwarning(
            "Missing Information",
            "Please fill Name, Roll Number, Course and Year."
        )
        return

    try:

        cursor.execute("""
            UPDATE students
            SET
                name=?,
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
            selected_id
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student updated successfully."
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Roll Number already exists."
        )


def delete_student():

    global selected_id

    if selected_id is None:

        messagebox.showwarning(
            "Select Student",
            "Please select a student first."
        )
        return

    answer = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if not answer:
        return

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (selected_id,)
    )

    conn.commit()

    messagebox.showinfo(
        "Deleted",
        "Student deleted successfully."
    )

    clear_fields()
    display_students()


def search_student():

    keyword = search_var.get().strip()

    if not keyword:

        display_students()
        return

    search_text = f"%{keyword}%"

    cursor.execute("""
        SELECT
            id,
            name,
            roll_no,
            course,
            year,
            phone,
            email
        FROM students
        WHERE
            name LIKE ?
            OR roll_no LIKE ?
            OR course LIKE ?
        ORDER BY id DESC
    """, (
        search_text,
        search_text,
        search_text
    ))

    rows = cursor.fetchall()

    display_students(rows)


def show_all():

    search_var.set("")
    display_students()
    clear_fields()


# =========================================================
# ATTENDANCE
# =========================================================

def show_attendance():

    window = tk.Toplevel(root)

    window.title("Attendance Management")
    window.geometry("900x650")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="Student Attendance",
        font=("Segoe UI", 24, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=(25, 5))

    tk.Label(
        window,
        text="Mark attendance for students",
        font=("Segoe UI", 11),
        bg=BG,
        fg=MUTED
    ).pack()

    date_frame = tk.Frame(
        window,
        bg=BG
    )

    date_frame.pack(pady=20)

    tk.Label(
        date_frame,
        text="Date:",
        font=("Segoe UI", 11, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(side="left", padx=5)

    date_entry = tk.Entry(
        date_frame,
        font=("Segoe UI", 11),
        width=20
    )

    date_entry.pack(
        side="left",
        padx=5,
        ipady=5
    )

    date_entry.insert(
        0,
        today_date()
    )

    students_frame = tk.Frame(
        window,
        bg=WHITE
    )

    students_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    attendance_vars = {}

    cursor.execute("""
        SELECT id, name, roll_no
        FROM students
        ORDER BY roll_no
    """)

    students = cursor.fetchall()

    if not students:

        tk.Label(
            students_frame,
            text="No students found.",
            font=("Segoe UI", 14),
            bg=WHITE,
            fg=MUTED
        ).pack(pady=50)

    else:

        header = tk.Frame(
            students_frame,
            bg=SIDEBAR
        )

        header.pack(fill="x")

        for text_value, width in [
            ("Roll No", 15),
            ("Student Name", 30),
            ("Attendance", 25)
        ]:

            tk.Label(
                header,
                text=text_value,
                width=width,
                bg=SIDEBAR,
                fg=WHITE,
                font=("Segoe UI", 10, "bold")
            ).pack(
                side="left",
                pady=10
            )

        for student_id, name, roll_no in students:

            row = tk.Frame(
                students_frame,
                bg=WHITE
            )

            row.pack(
                fill="x",
                pady=3
            )

            tk.Label(
                row,
                text=roll_no,
                width=15,
                bg=WHITE,
                fg=TEXT
            ).pack(side="left")

            tk.Label(
                row,
                text=name,
                width=30,
                anchor="w",
                bg=WHITE,
                fg=TEXT
            ).pack(side="left")

            var = tk.StringVar(
                value="Present"
            )

            attendance_vars[student_id] = var

            tk.Radiobutton(
                row,
                text="Present",
                variable=var,
                value="Present",
                bg=WHITE,
                fg=SUCCESS
            ).pack(
                side="left",
                padx=10
            )

            tk.Radiobutton(
                row,
                text="Absent",
                variable=var,
                value="Absent",
                bg=WHITE,
                fg=DANGER
            ).pack(
                side="left"
            )

    def save_attendance():

        date = date_entry.get().strip()

        if not date:

            messagebox.showwarning(
                "Missing Date",
                "Please enter attendance date."
            )
            return

        for student_id, var in attendance_vars.items():

            cursor.execute("""
                SELECT id
                FROM attendance
                WHERE student_id=? AND date=?
            """, (
                student_id,
                date
            ))

            existing = cursor.fetchone()

            if existing:

                cursor.execute("""
                    UPDATE attendance
                    SET status=?
                    WHERE student_id=? AND date=?
                """, (
                    var.get(),
                    student_id,
                    date
                ))

            else:

                cursor.execute("""
                    INSERT INTO attendance
                    (student_id, date, status)
                    VALUES (?, ?, ?)
                """, (
                    student_id,
                    date,
                    var.get()
                ))

        conn.commit()

        update_dashboard_stats()

        messagebox.showinfo(
            "Success",
            "Attendance saved successfully!"
        )

    tk.Button(
        window,
        text="SAVE ATTENDANCE",
        command=save_attendance,
        bg=SUCCESS,
        fg=WHITE,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        cursor="hand2",
        padx=25,
        pady=10
    ).pack(pady=20)


# =========================================================
# FEES
# =========================================================

def show_fees():

    window = tk.Toplevel(root)

    window.title("Fees Management")
    window.geometry("850x600")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="Fees Management",
        font=("Segoe UI", 24, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=25)

    form = tk.Frame(
        window,
        bg=WHITE
    )

    form.pack(
        fill="x",
        padx=30,
        pady=10
    )

    tk.Label(
        form,
        text="Student Roll No",
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).grid(
        row=0,
        column=0,
        padx=15,
        pady=15
    )

    roll_entry = tk.Entry(
        form,
        font=("Segoe UI", 11)
    )

    roll_entry.grid(
        row=0,
        column=1,
        padx=15,
        pady=15
    )

    tk.Label(
        form,
        text="Amount",
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).grid(
        row=1,
        column=0,
        padx=15,
        pady=15
    )

    amount_entry = tk.Entry(
        form,
        font=("Segoe UI", 11)
    )

    amount_entry.grid(
        row=1,
        column=1,
        padx=15,
        pady=15
    )

    tk.Label(
        form,
        text="Date",
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).grid(
        row=2,
        column=0,
        padx=15,
        pady=15
    )

    date_entry = tk.Entry(
        form,
        font=("Segoe UI", 11)
    )

    date_entry.grid(
        row=2,
        column=1,
        padx=15,
        pady=15
    )

    date_entry.insert(
        0,
        today_date()
    )

    tk.Label(
        form,
        text="Status",
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).grid(
        row=3,
        column=0,
        padx=15,
        pady=15
    )

    status_var = tk.StringVar(
        value="Paid"
    )

    ttk.Combobox(
        form,
        textvariable=status_var,
        values=["Paid", "Pending"],
        state="readonly",
        width=18
    ).grid(
        row=3,
        column=1,
        padx=15,
        pady=15
    )

    def save_fees():

        roll = roll_entry.get().strip()
        amount = amount_entry.get().strip()
        date = date_entry.get().strip()

        if not roll or not amount or not date:

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        try:

            amount_value = float(amount)

            cursor.execute(
                "SELECT id FROM students WHERE roll_no=?",
                (roll,)
            )

            student = cursor.fetchone()

            if not student:

                messagebox.showerror(
                    "Error",
                    "Student not found."
                )
                return

            cursor.execute("""
                INSERT INTO fees
                (student_id, amount, status, date)
                VALUES (?, ?, ?, ?)
            """, (
                student[0],
                amount_value,
                status_var.get(),
                date
            ))

            conn.commit()

            update_dashboard_stats()

            messagebox.showinfo(
                "Success",
                "Fees saved successfully!"
            )

            roll_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount."
            )

    tk.Button(
        window,
        text="SAVE FEES",
        command=save_fees,
        bg=SUCCESS,
        fg=WHITE,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        cursor="hand2",
        padx=25,
        pady=10
    ).pack(pady=20)


# =========================================================
# REPORTS
# =========================================================

def show_reports():

    window = tk.Toplevel(root)

    window.title("Student Reports")
    window.geometry("1000x600")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="Student Attendance Reports",
        font=("Segoe UI", 24, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=25)

    table_frame = tk.Frame(
        window,
        bg=WHITE
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    columns = (
        "Roll No",
        "Name",
        "Present",
        "Absent",
        "Total",
        "Percentage"
    )

    report_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        report_tree.heading(
            column,
            text=column
        )

        report_tree.column(
            column,
            width=140,
            anchor="center"
        )

    report_tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    cursor.execute("""
        SELECT id, name, roll_no
        FROM students
        ORDER BY roll_no
    """)

    students = cursor.fetchall()

    for student_id, name, roll_no in students:

        cursor.execute("""
            SELECT
                SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END),
                SUM(CASE WHEN status='Absent' THEN 1 ELSE 0 END)
            FROM attendance
            WHERE student_id=?
        """, (student_id,))

        result = cursor.fetchone()

        present = result[0] or 0
        absent = result[1] or 0

        total = present + absent

        percentage = (
            present / total * 100
            if total > 0
            else 0
        )

        report_tree.insert(
            "",
            tk.END,
            values=(
                roll_no,
                name,
                present,
                absent,
                total,
                f"{percentage:.2f}%"
            )
        )


# =========================================================
# DATABASE BACKUP
# =========================================================

def backup_database():

    try:

        backup_path = filedialog.asksaveasfilename(
            title="Save Database Backup",
            defaultextension=".db",
            filetypes=[
                ("SQLite Database", "*.db"),
                ("All Files", "*.*")
            ],
            initialfile="students_backup.db"
        )

        if not backup_path:
            return

        backup_conn = sqlite3.connect(
            backup_path
        )

        with backup_conn:
            conn.backup(backup_conn)

        backup_conn.close()

        messagebox.showinfo(
            "Backup Successful",
            "Database backup created successfully!"
        )

    except Exception as e:

        messagebox.showerror(
            "Backup Error",
            str(e)
        )


# =========================================================
# LOGIN
# =========================================================

def logout():

    answer = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if answer:
        show_login()


def exit_application():

    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:

        conn.close()
        root.destroy()


def show_login():

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("500x500")
    root.configure(bg=BG)

    frame = tk.Frame(
        root,
        bg=WHITE
    )

    frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        width=420,
        height=400
    )

    tk.Label(
        frame,
        text="STUDENT",
        font=("Segoe UI", 25, "bold"),
        bg=WHITE,
        fg=SIDEBAR
    ).pack(pady=(35, 0))

    tk.Label(
        frame,
        text="MANAGEMENT SYSTEM",
        font=("Segoe UI", 12, "bold"),
        bg=WHITE,
        fg=PRIMARY
    ).pack()

    tk.Label(
        frame,
        text="Admin Login",
        font=("Segoe UI", 11),
        bg=WHITE,
        fg=MUTED
    ).pack(pady=(8, 25))

    tk.Label(
        frame,
        text="Username",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=50)

    username_entry = tk.Entry(
        frame,
        font=("Segoe UI", 11)
    )

    username_entry.pack(
        fill="x",
        padx=50,
        pady=(5, 15),
        ipady=7
    )

    tk.Label(
        frame,
        text="Password",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=50)

    password_entry = tk.Entry(
        frame,
        font=("Segoe UI", 11),
        show="*"
    )

    password_entry.pack(
        fill="x",
        padx=50,
        pady=(5, 20),
        ipady=7
    )

    def login():

        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == "admin" and password == "admin123":

            open_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    tk.Button(
        frame,
        text="LOGIN",
        command=login,
        bg=PRIMARY,
        fg=WHITE,
        activebackground=PRIMARY_DARK,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        cursor="hand2"
    ).pack(
        fill="x",
        padx=50,
        ipady=8
    )

    tk.Label(
        frame,
        text="Username: admin  |  Password: admin123",
        font=("Segoe UI", 8),
        bg=WHITE,
        fg=MUTED
    ).pack(pady=15)

    username_entry.focus()


# =========================================================
# DASHBOARD
# =========================================================

def open_dashboard():

    global tree

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1250x750")

    # =====================================================
    # SIDEBAR
    # =====================================================

    sidebar = tk.Frame(
        root,
        bg=SIDEBAR,
        width=230
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)

    tk.Label(
        sidebar,
        text="SMS",
        font=("Segoe UI", 30, "bold"),
        bg=SIDEBAR,
        fg=WHITE
    ).pack(pady=(30, 0))

    tk.Label(
        sidebar,
        text="Student Management",
        font=("Segoe UI", 10),
        bg=SIDEBAR,
        fg="#bfdbfe"
    ).pack(pady=(0, 30))

    def sidebar_button(
        text_value,
        command,
        active=False
    ):

        tk.Button(
            sidebar,
            text="  " + text_value,
            anchor="w",
            command=command,
            font=("Segoe UI", 11, "bold" if active else "normal"),
            bg=SIDEBAR_HOVER if active else SIDEBAR,
            fg=WHITE if active else "#dbeafe",
            activebackground=SIDEBAR_HOVER,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            padx=25
        ).pack(
            fill="x",
            ipady=12,
            padx=10,
            pady=3
        )

    sidebar_button(
        "Dashboard",
        open_dashboard,
        True
    )

    sidebar_button(
        "Students",
        lambda: display_students()
    )

    sidebar_button(
        "Attendance",
        show_attendance
    )

    sidebar_button(
        "Fees",
        show_fees
    )

    sidebar_button(
        "Reports",
        show_reports
    )

    sidebar_button(
        "Database Backup",
        backup_database
    )

    tk.Frame(
        sidebar,
        bg=SIDEBAR
    ).pack(
        fill="both",
        expand=True
    )

    sidebar_button(
        "Logout",
        logout
    )

    sidebar_button(
        "Exit Application",
        exit_application
    )

    # =====================================================
    # MAIN AREA
    # =====================================================

    main_area = tk.Frame(
        root,
        bg=BG
    )

    main_area.pack(
        side="left",
        fill="both",
        expand=True
    )

    # =====================================================
    # HEADER
    # =====================================================

    header = tk.Frame(
        main_area,
        bg=WHITE,
        height=75
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Dashboard",
        font=("Segoe UI", 23, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        side="left",
        padx=30
    )

    tk.Label(
        header,
        text="Welcome, Admin",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=MUTED
    ).pack(
        side="right",
        padx=30
    )

    # =====================================================
    # CONTENT
    # =====================================================

    content = tk.Frame(
        main_area,
        bg=BG
    )

    content.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=18
    )

    # =====================================================
    # STATISTICS
    # =====================================================

    stats_frame = tk.Frame(
        content,
        bg=BG
    )

    stats_frame.pack(
        fill="x",
        pady=(0, 15)
    )

    def create_stat_card(
        parent,
        title,
        variable,
        subtitle,
        text_color
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            height=125
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=6
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        tk.Label(
            card,
            textvariable=variable,
            font=("Segoe UI", 23, "bold"),
            bg=WHITE,
            fg=text_color
        ).pack(
            anchor="w",
            padx=20
        )

        tk.Label(
            card,
            text=subtitle,
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=20
        )

    create_stat_card(
        stats_frame,
        "TOTAL STUDENTS",
        total_students_var,
        "Registered students",
        PRIMARY
    )

    create_stat_card(
        stats_frame,
        "TODAY PRESENT",
        today_present_var,
        today_date(),
        SUCCESS
    )

    create_stat_card(
        stats_frame,
        "FEES COLLECTED",
        total_fees_var,
        "Total paid fees",
        PURPLE
    )

    create_stat_card(
        stats_frame,
        "PENDING FEES",
        pending_fees_var,
        "Fees pending",
        WARNING
    )

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    quick_frame = tk.Frame(
        content,
        bg=WHITE
    )

    quick_frame.pack(
        fill="x",
        pady=(0, 15)
    )

    tk.Label(
        quick_frame,
        text="Quick Actions",
        font=("Segoe UI", 13, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        side="left",
        padx=20,
        pady=12
    )

    def quick_button(
        text_value,
        command,
        bg_color
    ):

        tk.Button(
            quick_frame,
            text=text_value,
            command=command,
            bg=bg_color,
            fg=WHITE,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6
        ).pack(
            side="right",
            padx=5,
            pady=8
        )

    quick_button(
        "Add Student",
        focus_student_form,
        PRIMARY
    )

    quick_button(
        "Attendance",
        show_attendance,
        SUCCESS
    )

    quick_button(
        "Fees",
        show_fees,
        WARNING
    )

    quick_button(
        "Reports",
        show_reports,
        PURPLE
    )

    # =====================================================
    # STUDENT FORM
    # =====================================================

    form_panel = tk.Frame(
        content,
        bg=WHITE
    )

    form_panel.pack(
        fill="x",
        pady=(0, 12)
    )

    tk.Label(
        form_panel,
        text="Student Information",
        font=("Segoe UI", 14, "bold"),
        bg=WHITE,
        fg=TEXT
    ).grid(
        row=0,
        column=0,
        columnspan=4,
        sticky="w",
        padx=20,
        pady=(12, 8)
    )

    labels = [
        ("Name", 1, 0),
        ("Roll Number", 1, 2),
        ("Course", 2, 0),
        ("Year", 2, 2),
        ("Phone", 3, 0),
        ("Email", 3, 2)
    ]

    for text_value, row, col in labels:

        tk.Label(
            form_panel,
            text=text_value,
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=MUTED
        ).grid(
            row=row,
            column=col,
            sticky="w",
            padx=(20, 8),
            pady=4
        )

    tk.Entry(
        form_panel,
        textvariable=name_var,
        font=("Segoe UI", 10)
    ).grid(
        row=1,
        column=1,
        sticky="ew",
        padx=5,
        pady=4,
        ipady=4
    )

    tk.Entry(
        form_panel,
        textvariable=roll_var,
        font=("Segoe UI", 10)
    ).grid(
        row=1,
        column=3,
        sticky="ew",
        padx=(5, 20),
        pady=4,
        ipady=4
    )

    tk.Entry(
        form_panel,
        textvariable=course_var,
        font=("Segoe UI", 10)
    ).grid(
        row=2,
        column=1,
        sticky="ew",
        padx=5,
        pady=4,
        ipady=4
    )

    ttk.Combobox(
        form_panel,
        textvariable=year_var,
        values=[
            "First Year",
            "Second Year",
            "Third Year",
            "Final Year"
        ],
        state="readonly"
    ).grid(
        row=2,
        column=3,
        sticky="ew",
        padx=(5, 20),
        pady=4,
        ipady=3
    )

    tk.Entry(
        form_panel,
        textvariable=phone_var,
        font=("Segoe UI", 10)
    ).grid(
        row=3,
        column=1,
        sticky="ew",
        padx=5,
        pady=4,
        ipady=4
    )

    tk.Entry(
        form_panel,
        textvariable=email_var,
        font=("Segoe UI", 10)
    ).grid(
        row=3,
        column=3,
        sticky="ew",
        padx=(5, 20),
        pady=4,
        ipady=4
    )

    form_panel.columnconfigure(1, weight=1)
    form_panel.columnconfigure(3, weight=1)

    button_frame = tk.Frame(
        form_panel,
        bg=WHITE
    )

    button_frame.grid(
        row=4,
        column=0,
        columnspan=4,
        sticky="e",
        padx=20,
        pady=10
    )

    tk.Button(
        button_frame,
        text="Add Student",
        command=add_student,
        bg=SUCCESS,
        fg=WHITE,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=6
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="Update",
        command=update_student,
        bg=PRIMARY,
        fg=WHITE,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=6
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="Delete",
        command=delete_student,
        bg=DANGER,
        fg=WHITE,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=6
    ).pack(side="left", padx=4)

    tk.Button(
        button_frame,
        text="Clear",
        command=clear_fields,
        bg="#64748b",
        fg=WHITE,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=6
    ).pack(side="left", padx=4)

    # =====================================================
    # SEARCH
    # =====================================================

    search_frame = tk.Frame(
        content,
        bg=BG
    )

    search_frame.pack(
        fill="x",
        pady=(0, 8)
    )

    tk.Label(
        search_frame,
        text="Search Students",
        font=("Segoe UI", 12, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(side="left")

    tk.Entry(
        search_frame,
        textvariable=search_var,
        font=("Segoe UI", 10)
    ).pack(
        side="left",
        padx=15,
        ipady=5,
        fill="x",
        expand=True
    )

    tk.Button(
        search_frame,
        text="Search",
        command=search_student,
        bg=PRIMARY,
        fg=WHITE,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=6
    ).pack(side="left", padx=4)

    tk.Button(
        search_frame,
        text="Show All",
        command=show_all,
        bg="#64748b",
        fg=WHITE,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=6
    ).pack(side="left", padx=4)

    # =====================================================
    # STUDENT TABLE
    # =====================================================

    table_frame = tk.Frame(
        content,
        bg=WHITE
    )

    table_frame.pack(
        fill="both",
        expand=True
    )

    columns = (
        "ID",
        "Name",
        "Roll No",
        "Course",
        "Year",
        "Phone",
        "Email"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    widths = {
        "ID": 50,
        "Name": 150,
        "Roll No": 100,
        "Course": 120,
        "Year": 110,
        "Phone": 120,
        "Email": 200
    }

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=widths[column],
            anchor="center"
        )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=10
    )

    scrollbar.pack(
        side="right",
        fill="y",
        padx=(0, 10),
        pady=10
    )

    tree.bind(
        "<<TreeviewSelect>>",
        select_student
    )

    # =====================================================
    # STYLE
    # =====================================================

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except:
        pass

    style.configure(
        "Treeview",
        background=WHITE,
        foreground=TEXT,
        rowheight=32,
        fieldbackground=WHITE,
        font=("Segoe UI", 9)
    )

    style.configure(
        "Treeview.Heading",
        background=SIDEBAR,
        foreground=WHITE,
        font=("Segoe UI", 9, "bold"),
        padding=8
    )

    style.map(
        "Treeview",
        background=[
            ("selected", "#dbeafe")
        ],
        foreground=[
            ("selected", TEXT)
        ]
    )

    display_students()
    update_dashboard_stats()


# =========================================================
# QUICK ADD STUDENT
# =========================================================

def focus_student_form():

    name_var.set("")
    roll_var.set("")
    course_var.set("")
    year_var.set("")
    phone_var.set("")
    email_var.set("")

    messagebox.showinfo(
        "Add Student",
        "Student Information form is ready.\n\nFill the details and click Add Student."
    )


# =========================================================
# SPLASH SCREEN
# =========================================================

def show_splash():

    root.withdraw()

    splash = tk.Toplevel(root)

    splash.overrideredirect(True)
    splash.configure(bg=SIDEBAR)

    width = 600
    height = 350

    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    splash.geometry(
        f"{width}x{height}+{x}+{y}"
    )

    tk.Label(
        splash,
        text="🎓",
        font=("Segoe UI Emoji", 55),
        bg=SIDEBAR,
        fg=WHITE
    ).pack(pady=(40, 5))

    tk.Label(
        splash,
        text="Student Management System",
        font=("Segoe UI", 25, "bold"),
        bg=SIDEBAR,
        fg=WHITE
    ).pack()

    tk.Label(
        splash,
        text="Smart • Simple • Professional",
        font=("Segoe UI", 12),
        bg=SIDEBAR,
        fg="#bfdbfe"
    ).pack(pady=8)

    tk.Label(
        splash,
        text="Loading application...",
        font=("Segoe UI", 10),
        bg=SIDEBAR,
        fg="#dbeafe"
    ).pack(pady=(15, 5))

    progress = ttk.Progressbar(
        splash,
        orient="horizontal",
        length=350,
        mode="determinate"
    )

    progress.pack(pady=5)

    def animate(value=0):

        if value <= 100:

            progress["value"] = value

            splash.after(
                20,
                lambda: animate(value + 2)
            )

        else:

            splash.destroy()
            root.deiconify()
            show_login()

    splash.after(
        100,
        animate
    )


# =========================================================
# START
# =========================================================

root.protocol(
    "WM_DELETE_WINDOW",
    exit_application
)

show_splash()

root.mainloop()