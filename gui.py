import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import time

face_recognition_process = None

def set_status(text, color):
    status_label.config(text=text, fg=color)

def start_recognition():
    global face_recognition_process
    script_path = r'C:\Users\choug\PycharmProjects\FaceRecognition\main.py'
    try:
        face_recognition_process = subprocess.Popen(["python", script_path])
        set_status("Recognition started.", "green")
        for i in range(101):
            progress.set(i)
            root.update_idletasks()
            time.sleep(0.03)
    except Exception as e:
        messagebox.showerror("Error", f"Could not start face recognition.\n{e}")
        set_status("Error starting recognition.", "red")

def stop_recognition():
    global face_recognition_process
    if face_recognition_process:
        if messagebox.askyesno("Confirmation", "Are you sure you want to stop recognition?"):
            face_recognition_process.terminate()
            face_recognition_process = None
            set_status("Recognition stopped.", "red")
        else:
            set_status("Recognition still running.", "green")

def on_closing():
    stop_recognition()
    if messagebox.askokcancel("Exit", "Do you want to Exit?"):
        root.destroy()

root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("400x300")
root.configure(bg="Light gray")

headline_label = tk.Label(root, text=" FACE RECOGNITION ", font=("Arial", 20, "bold"), fg="white", bg="black")
headline_label.pack(pady=10)

start_button = tk.Button(root, text="Start Recognition", command=start_recognition, bg="green", fg="white", relief=tk.RAISED, bd=3)
start_button.pack(pady=20)

stop_button = tk.Button(root, text="Stop Recognition", command=stop_recognition, bg="red", fg="white", relief=tk.RAISED, bd=3)
stop_button.pack(pady=20)

status_label = tk.Label(root, text="Status: Not running", bg="lightgray")
status_label.pack(pady=20)

progress = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress, maximum=100, length=200, mode="determinate",
                               style="TProgressbar.Horizontal.TProgressbar")
progress_bar.pack()

style = ttk.Style()
style.configure("TProgressbar.Horizontal.TProgressbar", troughcolor="lightgray", background="green", thickness=20)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
