import time
from tkinter import messagebox
from features import save_answers
from GUI import create_gui


def start(username, password, course_id):
    try:
        course_id = int(course_id)
    except ValueError:
        messagebox.showerror("Input Error", "Course ID must be a number")
        return

    q_time = 10  # Fixed time per question in seconds

    if not username or not password:
        messagebox.showerror("Input Error", "Username and password cannot be empty")
        return

    save_answers(username, password, course_id, q_time)
    messagebox.showinfo("Success", "Answers saved successfully!")

    time.sleep(150)  # Optional delay


if __name__ == "__main__":
    create_gui(start)