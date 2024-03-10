import pyttsx3
from tkinter import *
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle  # Import ThemedStyle from ttkthemes
import json
import time

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

class Quiz:
    def __init__(self):
        self.q_no = 0
        self.start_time = 0
        self.create_start_screen()

    def create_start_screen(self):
        self.start_frame = Frame(gui, width=800, height=500, bg="#4CAF50")
        self.start_frame.grid(row=0, column=0)

        title = Label(self.start_frame, text="QUIZ BOT",
                      width=50, bg="#4CAF50", fg="white", font=("Arial", 20, "bold"))
        title.place(x=0, y=2)

        self.subject_var = StringVar()

        # Use ThemedStyle for the dropdown
        style = ThemedStyle(self.start_frame)
        style.set_theme("radiance")  # Use "radiance" theme for cylindrical dropdown

        subject_label = Label(self.start_frame, text="Topic:",
                              width=15, bg="#4CAF50", fg="white", font=("cabriel", 18))
        subject_label.place(x=250, y=200)

        subjects = ["Sports", "General", "History"]  # Add your subjects here
        subject_dropdown = ttk.Combobox(self.start_frame, textvariable=self.subject_var, values=subjects, state="readonly", font=("Arial", 14))
        subject_dropdown.set("Select Topic")
        subject_dropdown.place(x=400, y=200)

        start_button = Button(self.start_frame, text="Start Quiz", command=self.start_quiz,
                              width=20, bg="#FF5733", fg="white", font=("Arial", 16, "bold"))
        start_button.place(x=300, y=300)

    def start_quiz(self):
        selected_subject = self.subject_var.get()

        if selected_subject == "Select Topic":
            messagebox.showinfo("Error", "Please select a subject.")
            return

        self.start_frame.destroy()  # Destroy the start screen
        self.load_data(selected_subject)
        self.display_title()
        self.display_question()
        self.opt_selected = IntVar()
        self.opts = self.radio_buttons()
        self.display_options()
        self.buttons()
        self.data_size = len(question)
        self.correct = 0
        self.create_progress_bar()
        self.start_time = time.time()

    # ... (rest

    def load_data(self, subject):
        # Load the data from the json file based on the selected subject
        filename = f'{subject.lower()}_data.json'
        with open(filename) as f:
            data = json.load(f)

        # Set the question, options, and answer
        global question, options, answer
        question = (data['question'])
        options = (data['options'])
        answer = (data['answer'])

    def display_result(self):
        wrong_count = self.data_size - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"
        score = int(self.correct / self.data_size * 100)
        result = f"Score: {score}%"
        avg_time_per_question = (time.time() - self.start_time) / self.data_size
        result += f"\nAverage Time per Question: {avg_time_per_question:.2f} seconds"
        result_text = f"{result}\n{correct}\n{wrong}"

        # Display the result in a label
        result_label = Label(gui, text=result_text, width=60, font=('Arial', 16, 'bold'), anchor='w', bg="#FFD700")
        result_label.place(x=70, y=150)

        # Speak the result
        speak(result_text)

        # Display a messagebox for the result
        messagebox.showinfo("Result", result_text)

    def check_ans(self, q_no):
        if self.opt_selected.get() == answer[q_no]:
            return True

    def next_btn(self):
        if self.check_ans(self.q_no):
            self.correct += 1

        self.q_no += 1

        if self.q_no == self.data_size:
            self.display_result()
            gui.destroy()
        else:
            self.display_question()
            self.display_options()
            self.update_progress()

    def buttons(self):
        next_button = Button(gui, text="Next", command=self.next_btn,
                             width=10, bg="#4CAF50", fg="white", font=("Arial", 16, "bold"))
        next_button.place(x=350, y=380)

        quit_button = Button(gui, text="Quit", command=gui.destroy,
                             width=5, bg="#FF5733", fg="white", font=("Arial", 16, " bold"))
        quit_button.place(x=700, y=50)

    def display_options(self):
        val = 0
        self.opt_selected.set(0)
        for option in options[self.q_no]:
            self.opts[val]['text'] = option
            self.opts[val]['bg'] = "#FFFFFF"  # Set the background color of options to white
            val += 1

    def display_question(self):
        q_no = Label(gui, text=question[self.q_no], width=60,
                     font=('Arial', 16, 'bold'), anchor='w', bg="#FFD700")
        q_no.place(x=70, y=100)

    def display_title(self):
        speak("WELCOME TO QUIZ BOT")
        title = Label(gui, text="QUIZ BOT",
                      width=50, bg="#4CAF50", fg="white", font=("Arial", 20, "bold"))
        title.place(x=0, y=2)

    def radio_buttons(self):
        q_list = []
        y_pos = 150
        while len(q_list) < 4:
            radio_btn = Radiobutton(gui, text=" ", variable=self.opt_selected,
                                    value=len(q_list)+1, font=("Arial", 14))
            q_list.append(radio_btn)
            radio_btn.place(x=100, y=y_pos)
            y_pos += 40
        return q_list

    def create_progress_bar(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar",
                        thickness=30,
                        troughcolor="#FFD700",
                        background="#4CAF50")

        self.progress_bar = ttk.Progressbar(gui, orient="horizontal", length=600, mode="determinate", style="TProgressbar")
        self.progress_bar.place(x=100, y=350)
        self.progress_bar["maximum"] = self.data_size
        self.progress_bar["value"] = 0

    def update_progress(self):
        self.progress_bar["value"] = self.q_no

# Create a GUI Window
gui = Tk()
gui.geometry("800x500")
gui.title("Ncet Quizzz")

# Set a light theme
style = ThemedStyle(gui)
style.set_theme("clam")

# Create an object of the Quiz Class
quiz = Quiz()

# Start the GUI
gui.mainloop()
