import tkinter as tk



def create_gui(start_saving):
    root = tk.Tk()
    root.title("Course Answer Saver")

    # Center the window
    window_width = 300
    window_height = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Username label and entry
    tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    # Password label and entry
    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    # Course ID label and entry
    tk.Label(root, text="Course ID:").grid(row=2, column=0, padx=10, pady=5)
    course_id_entry = tk.Entry(root)
    course_id_entry.grid(row=2, column=1, padx=10, pady=5)

    # Checkboxes
    complete_course_var = tk.BooleanVar()
    complete_tests_var = tk.BooleanVar()

    complete_course_cb = tk.Checkbutton(root, text="Complete Course", variable=complete_course_var)
    complete_course_cb.grid(row=3, column=0, columnspan=2, pady=5)

    complete_tests_cb = tk.Checkbutton(root, text="Complete Tests", variable=complete_tests_var)
    complete_tests_cb.grid(row=4, column=0, columnspan=2, pady=5)

    # Difficulty slider
    tk.Label(root, text="Difficulty:").grid(row=5, column=0, padx=10, pady=5)
    difficulty_var = tk.IntVar(value=1)
    difficulty_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, variable=difficulty_var)
    difficulty_slider.grid(row=5, column=1, padx=10, pady=5)

    # Submit button
    def on_submit():
        COURSES = complete_course_var.get()
        TESTS = complete_tests_var.get()
        DIFFICULTY = difficulty_var.get()


        # check inputs and validity

        start_saving(
            username_entry.get(),
            password_entry.get(),
            course_id_entry.get()
        )

    submit_button = tk.Button(root, text="Start", command=on_submit)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    root.mainloop()