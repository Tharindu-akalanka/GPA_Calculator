from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, StringVar, OptionMenu

OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("675x750")
window.configure(bg="#D2E2E2")
window.resizable(False, False)
window.title("GPA Calculator")

canvas = Canvas(window, bg="#D2E2E2", height=750, width=675, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

# White course container background
course_box = canvas.create_rectangle(51, 105, 623, 500, fill="#FFFFFF", outline="")

# GPA display bar
gpa_bar = canvas.create_rectangle(51, 630, 623, 700, fill="#046865", outline="")
gpa_label = canvas.create_text(107, 651, anchor="nw", text="Semester GPA", fill="#F2F7F7", font=("Rubik Medium", 24 * -1))
gpa_display = canvas.create_text(513, 651, anchor="nw", text="0.00", fill="#F2F7F7", font=("Rubik Medium", 24 * -1))

canvas.create_text(51, 32, anchor="nw", text="GPA CALCULATOR", fill="#03045E", font=("Rubik Bold", 36 * -1))
canvas.create_text(98, 184, anchor="nw", text="Module Name", fill="#046865", font=("Rubik Bold", 18 * -1))
canvas.create_text(308, 184, anchor="nw", text="Grade", fill="#046865", font=("Rubik Bold", 18 * -1))
canvas.create_text(440, 184, anchor="nw", text="Credits", fill="#046865", font=("Rubik Bold", 18 * -1))

grades_dict = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "F": 0.0
}

credits_options = ["Select", "0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4"]

rows = []
start_y = 219
max_courses = 7

def reposition_buttons_and_resize():
    white_box_left = 51
    white_box_width = 623 - white_box_left
    button_width = 100

    calc_x = white_box_left + (white_box_width // 2) - (button_width // 2)
    add_x = 285

    # Place buttons at fixed distance from bottom of white box
    gap_after_box = 20
    base_y = start_y + 30

    button_add.place(x=add_x, y=base_y + gap_after_box)
    button_calc.place(x=calc_x, y=base_y + gap_after_box + 45)

    # Move GPA bar below buttons
    canvas.coords(gpa_bar, 51, base_y + gap_after_box + 90, 623, base_y + gap_after_box + 160)
    canvas.coords(gpa_label, 107, base_y + gap_after_box + 110)
    canvas.coords(gpa_display, 513, base_y + gap_after_box + 110)

    # Resize window
    window.geometry(f"675x{base_y + gap_after_box + 170}")

def add_row():
    global start_y

    if len(rows) >= max_courses:
        return

    # Module Name Entry with default text
    course_entry = Entry(window, bg="#D2E1E1", bd=0, fg="gray")
    course_entry.insert(0, "Enter Module Name")
    course_entry.place(x=98, y=start_y, width=175, height=35)

    def on_focus_in(event, entry=course_entry):
        if entry.get() == "Enter Module Name":
            entry.delete(0, "end")
            entry.config(fg="black")

    course_entry.bind("<FocusIn>", on_focus_in)

    # Grade Dropdown
    grade_var = StringVar()
    grade_var.set("Select")
    grade_menu = OptionMenu(window, grade_var, *grades_dict.keys())
    grade_menu.config(bg="#D2E1E1", bd=0, highlightthickness=0, indicatoron=True)
    grade_menu.place(x=308, y=start_y, width=97, height=35)

    # Credit Dropdown
    credit_var = StringVar()
    credit_var.set("Select")
    credit_menu = OptionMenu(window, credit_var, *credits_options)
    credit_menu.config(bg="#D2E1E1", bd=0, highlightthickness=0, indicatoron=True)
    credit_menu.place(x=440, y=start_y, width=97, height=35)

    rows.append((course_entry, grade_var, credit_var))
    start_y += 49

    # Resize white box
    canvas.coords(course_box, 51, 105, 623, start_y + 30)

    # Reposition buttons and GPA bar
    reposition_buttons_and_resize()

def calculate_gpa():
    total_points = 0
    total_credits = 0
    for course, grade_var, credit_var in rows:
        grade = grade_var.get()
        credit = credit_var.get()
        if grade not in grades_dict or credit == "Select":
            continue
        try:
            credit_val = float(credit)
            total_credits += credit_val
            total_points += grades_dict[grade] * credit_val
        except ValueError:
            continue
    gpa = total_points / total_credits if total_credits > 0 else 0.0
    canvas.itemconfig(gpa_display, text=f"{gpa:.2f}")

# Load button images
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))

# Add Course Button
button_add = Button(image=button_image_7, borderwidth=0, highlightthickness=0, command=add_row, relief="flat")

# Calculate Button
button_calc = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=calculate_gpa, relief="flat")

# Add first 5 rows
for _ in range(5):
    add_row()

window.mainloop()
