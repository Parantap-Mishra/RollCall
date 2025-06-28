import tkinter as tk
from tkinter import filedialog, messagebox #file selction dialogue box (selectign and uploading image from desktop), pop up msg for confirmation
import cv2 #open cv
from PIL import Image, ImageTk #pillow for image processing
import pandas as pd
import numpy as np
import threading #runs training in the background
import os # allows file operations (checking paths, saving files).
import openpyxl
import time
from tkinter import ttk  # progress bar support
import datetime

# Coluors
BG_COLOR = "#F5F5F5"  # light gray background
TEXT_COLOR = "#003366"  # dark blue text
BTN_COLOR = "#4B74FF"  # vibrant blue buttons
ENTRY_COLOR = "#E0E0E0"  # light gray entry fields

# Initialize Main Window
root = tk.Tk()
root.title("Attendance System")
root.geometry("900x600")
root.configure(bg=BG_COLOR)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Content Wrapper
content = tk.Frame(root, bg=BG_COLOR)
content.grid(row=0, column=0, sticky="nsew")
content.grid_rowconfigure(0, weight=1)
content.grid_columnconfigure(0, weight=1)

# Defining frames for diff sections
menu_frame = tk.Frame(content, bg=BG_COLOR)
register_frame = tk.Frame(content, bg=BG_COLOR)
attendance_frame = tk.Frame(content, bg=BG_COLOR)

# function to switch frames
def show_frame(frame):
    frame.tkraise()

# Stack all frames in the same position
for frame in (menu_frame, register_frame, attendance_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# ------------------ Main Menu Section ------------------
menu_frame.grid_rowconfigure(0, weight=1)
menu_frame.grid_columnconfigure(0, weight=1)

main_container = tk.Frame(menu_frame, bg=BG_COLOR)
main_container.grid(row=0, column=0, sticky="nsew")
main_container.grid_columnconfigure(0, weight=1)

header = tk.Label(main_container, text="Attendance System", font=("Arial", 24, "bold"), bg=BTN_COLOR, fg="white", pady=20)
header.pack(fill="x")

register_card = tk.Frame(main_container, bg="white", bd=2, relief="groove")
register_card.pack(pady=30, padx=200, fill="x")
tk.Label(register_card, text="Register New Student", font=("Arial", 16, "bold"), bg="white", fg=BTN_COLOR).pack(pady=(10, 5))
tk.Button(register_card, text="Capture via Webcam", command=lambda: show_frame(register_frame),
          bg=BTN_COLOR, fg="white", font=("Arial", 12, "bold"), width=20, height=2).pack(pady=(5, 15))

take_attendance_card = tk.Frame(main_container, bg="white", bd=2, relief="groove")
take_attendance_card.pack(pady=10, padx=200, fill="x")
tk.Label(take_attendance_card, text="Take Attendance", font=("Arial", 16, "bold"), bg="white", fg=BTN_COLOR).pack(pady=(10, 5))
tk.Button(take_attendance_card, text="Start Attendance", command=lambda: show_frame(attendance_frame),
          bg=BTN_COLOR, fg="white", font=("Arial", 12, "bold"), width=20, height=2).pack(pady=(5, 15))

tk.Button(main_container, text="Exit", command=root.quit,
          bg="red", fg="white", font=("Arial", 12, "bold"), width=20, height=2).pack(pady=30)

# Sidebar for internal pages (register & attendance)
sidebar = tk.Frame(content, width=200, bg=BTN_COLOR)

# Sidebar Buttons
tk.Label(sidebar, text="Menu", bg=BTN_COLOR, fg="white", font=("Arial", 16, "bold")).pack(pady=20)
tk.Button(sidebar, text="Register Students", command=lambda: show_frame(register_frame), width=20, height=2, bg="white", fg=BTN_COLOR).pack(pady=10)
tk.Button(sidebar, text="Take Attendance", command=lambda: show_frame(attendance_frame), width=20, height=2, bg="white", fg=BTN_COLOR).pack(pady=10)
tk.Button(sidebar, text="Exit", command=root.quit, width=20, height=2, bg="red", fg="white").pack(pady=10)

# Layout for register_frame and attendance_frame with sidebar
register_frame.grid_columnconfigure(1, weight=1)
register_frame.grid_rowconfigure(0, weight=1)

attendance_frame.grid_columnconfigure(1, weight=1)
attendance_frame.grid_rowconfigure(0, weight=1)

sidebar.grid(row=0, column=0, sticky="ns")
# Stack all frames in the same position
for frame in (menu_frame, register_frame, attendance_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# Function to toggle sidebar visibility
def toggle_sidebar(show):
    if show:
        sidebar.grid()
    else:
        sidebar.grid_remove()
# function to switch frames
def show_frame(frame):
    frame.tkraise()
    if frame == menu_frame:
        toggle_sidebar(False)
    else:
        toggle_sidebar(True)


# ------------------ Register Student Section ------------------
for widget in register_frame.winfo_children():
    widget.destroy()

register_inner = tk.Frame(register_frame, bg=BG_COLOR)
register_inner.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(register_inner, text="Student Registration", font=("Arial", 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=2, pady=20)

tk.Label(register_inner, text="Student Name:", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="e")
name_entry = tk.Entry(register_inner, width=30, bg=ENTRY_COLOR, font=("Arial", 12))
name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(register_inner, text="Student ID:", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="e")
id_entry = tk.Entry(register_inner, width=30, bg=ENTRY_COLOR, font=("Arial", 12))
id_entry.grid(row=2, column=1, padx=10, pady=5)

image_label = tk.Label(register_inner, bg=BG_COLOR)
image_label.grid(row=3, column=0, columnspan=2, pady=10)



# function to Capture Image
def capture_images():
    cap = cv2.VideoCapture(0)  # Open webcam (0 = default camera)
    name = name_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Please enter Student Name before capturing images!")
        return

    # create dataset folder if it doesn't exist
    dataset_path = f"dataset/{name}"
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    count = 0  # counter for image count

    while True:
        ret, frame = cap.read()  # Read frame from webcam
        if not ret:  # ret is boolean which returns True if the frame is successfully captured.
            break   # breaks loop if frame not found

        cv2.imshow("Press Space to start capturing Images - Look at the camera", frame)  # Open window with webcam titled "press space...."

        key = cv2.waitKey(1)  # waits for a key press
        if key == 32:  # checks if spacebar pressed
            while count < 30:  # capture 30 images
                ret, frame = cap.read()  # Read frame from webcam again
                if not ret:  
                    break   

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert image to grayscale
                image_path = f"{dataset_path}/{count}.jpg"
                cv2.imwrite(image_path, gray)  # save image
                count += 1

                cv2.imshow("Capturing...", frame)
                cv2.waitKey(100)  # Wait for 100ms between captures
            break  # Exit after capturing 30 images
        elif key == 27:  # Esc key to exit without capturing
            break

    cap.release()  # Stops webcam
    cv2.destroyAllWindows()  # Destroys all opencv windows

    messagebox.showinfo("Success", "Images captured successfully! Training will now begin.")

    train_model()  # start training process

    # Saving Student Data

    student_id = id_entry.get().strip()  # Gets id from label and removes whitespaces

    if not name or not student_id:
        messagebox.showerror("Error", "Please enter both Name and ID before capturing!")
        return

    # Check if the file exists
    file_exists = os.path.isfile("students.xlsx")

    if file_exists:
        # loads existing workbook
        wb = openpyxl.load_workbook("students.xlsx")
        sheet = wb.active
    else:
        # creates a new workbook
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["Name", "ID"])  # column headers

    # appends new student data
    sheet.append([name, student_id])
    wb.save("students.xlsx")  # saves the file
    wb.close()

    # clears fields after Saving
    name_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)

# Train Model Function
def train_model():
    progress_window = tk.Toplevel(root)  # Creates a new window for progress
    progress_window.title("Training Model")
    progress_window.geometry("300x100")
    
    tk.Label(progress_window, text="Training in progress...", font=("Arial", 12)).pack(pady=10)
    
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=250, mode="determinate") #The mode="determinate" allows incremental updates as training progresses.
    progress_bar.pack(pady=10)
    
    def run_training():
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # Creates the LBPH face recognizer
        faces = []
        ids = []
        label_data = []

        student_list = os.listdir("dataset/")  # Reads all student folders. Each folder represents one student's images.
        total_students = len(student_list)
        progress_bar["maximum"] = total_students

        for index, student in enumerate(student_list):
            student_path = f"dataset/{student}"
            image_files = os.listdir(student_path)

            for image_file in image_files:
                image_path = f"{student_path}/{image_file}"
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                faces.append(img)
                ids.append(index)

            # Find ID from Excel
            student_df = pd.read_excel("students.xlsx")
            student_id_row = student_df[student_df["Name"] == student]
            student_id = student_id_row["ID"].values[0] if not student_id_row.empty else "Unknown"

            label_data.append([index, student, student_id])

            progress_bar["value"] = index + 1
            progress_window.update_idletasks()

        recognizer.train(faces, np.array(ids))
        recognizer.save("trainer.yml")  # Save trained model

        # saves label mappings to labels.csv
        df = pd.DataFrame(label_data, columns=["label", "name", "id"])
        df.to_csv("labels.csv", index=False)

        progress_window.destroy()
        messagebox.showinfo("Success", "Training completed! The system is now ready for attendance tracking.")

    threading.Thread(target=run_training).start()  # Run training function in a separate thread or execution path. This is done so that: The GUI remains responsive. The teacher sees real-time progress updates.

    

capture_btn = tk.Button(
    register_inner, text="Capture via Webcam", command=capture_images,
    bg=BTN_COLOR, fg="white", font=("Arial", 12, "bold"), width=20
)
capture_btn.grid(row=4, column=0, columnspan=2, pady=10)

tk.Button(register_inner, text="Back to Main Menu", command=lambda: show_frame(menu_frame),
          width=20, height=2, bg=BTN_COLOR, fg="white", font=("Arial", 10)).grid(row=5, column=0, columnspan=2, pady=10)



# ------------- Attendance frame ----------------
def recognize_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # Creates the LBPH face recognizer
    recognizer.read("trainer.yml")  # Load trained model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")  # Uses opencv's pre-trained face detection model to find faces in the webcam feed.

    cap = cv2.VideoCapture(0)  # Open webcam

    students_data = pd.read_excel("students.xlsx")  # Load student data
    today = datetime.date.today().strftime("%d-%b-%Y")  

    # Add new column for today's date if not already present
    if today not in students_data.columns:
        students_data[today] = ""

    recognized = False  # Flag to exit loop if face is recognized
    recognized_name = None  # matched student name
    recognized_time = None  # time of recognition

    start_time = time.time()  # timer to track how long the system runs

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)  # Finds faces using opencv's face detection model

        for (x, y, w, h) in faces:  # loops through each detected face’s coordinates
            face_roi = gray[y:y+h, x:x+w]  # Extract face region
            label, confidence = recognizer.predict(face_roi)  # Recognize face. Label returns student index and confidence returns accuracy %

            if confidence < 70:  # Confidence threshold for recognition
                recognized = True

                # Load label mapping from labels.csv
                label_df = pd.read_csv("labels.csv")
                matched_row = label_df[label_df["label"] == label]

                if not matched_row.empty:
                    recognized_name = matched_row["name"].values[0]
                    student_id = matched_row["id"].values[0]

                    # Find the correct row in Excel by ID
                    excel_row = students_data[students_data["ID"] == student_id]
                    if not excel_row.empty:
                        students_data.loc[excel_row.index[0], today] = "Yes"

                if recognized_time is None:  
                    recognized_time = time.time()  #time of recognition

            # face box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Show name if recognized
            if recognized and recognized_name:
                cv2.putText(frame, f"{recognized_name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Face Recognition - Attendance Tracking", frame)  # Displays the live webcam feed with recognized student names on top

        key = cv2.waitKey(1)  # refresh the opencv window

        current_time = time.time()

        if not recognized and (current_time - start_time) > 60:  # After 60 seconds, if no face matched
            messagebox.showinfo("Result", "Not a student from your class.")
            break

        if recognized and (current_time - recognized_time) > 5:  # Show the matched face for 5 seconds, then exits
            messagebox.showinfo("Success", f"Attendance marked for {recognized_name} on {today}")
            break

    cap.release()  
    cv2.destroyAllWindows()  
    students_data.to_excel("students.xlsx", index=False)  # Save updated attendance
# ------------- Attendance Section ----------------
for widget in attendance_frame.winfo_children():
    widget.destroy()

attendance_inner = tk.Frame(attendance_frame, bg=BG_COLOR)
attendance_inner.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(attendance_inner, text="Attendance System", font=("Arial", 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

tk.Button(attendance_inner, text="Take Attendance", command=recognize_faces,
          width=20, height=2, bg=BTN_COLOR, fg="white", font=("Arial", 12, "bold")).pack(pady=10)

tk.Button(attendance_inner, text="Back to Main Menu", command=lambda: show_frame(menu_frame),
          width=20, height=2, bg=BTN_COLOR, fg="white", font=("Arial", 10)).pack(pady=10)

# Stack all frames in the same position
for frame in (menu_frame, register_frame, attendance_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# Show Main Menu initially
show_frame(menu_frame)

# Run the Tkinter loop
root.mainloop()
