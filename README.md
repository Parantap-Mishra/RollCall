# 📸 RollCall: Face Recognition Attendance System

### A computer vision-based attendance tracker for classrooms, using facial recognition.

---

## 🧾 Overview

This is a **Tkinter-based GUI application** that uses **OpenCV** and **LBPH Face Recognition** to automate attendance tracking through facial recognition. The system captures face data of each student, trains a local model, and marks attendance upon successful face identification — all stored in an Excel sheet.

I am presenting this project to my school for potential integration into some classrooms as a tech-driven solution to reduce manual attendance efforts.

> ⚠️ **Note**: This is the most basic version of the project. The current facial recognition system is not 100% accurate and may sometimes give false positives/negatives. I’m actively working on making it more reliable and efficient.

---

## 💡 Features

* Register new students using webcam
* Capture 30 grayscale face images per student for training
* Train a face recognition model using **LBPH (Local Binary Pattern Histogram)**
* Live attendance tracking through webcam
* Attendance is saved automatically in an Excel sheet, with date-wise tracking
* Clean, interactive Tkinter GUI

---

## 🛠️ Tech Stack

* **Python 3.13.5**
* **Tkinter** – GUI
* **OpenCV** – Image capture and recognition
* **Pandas** & **OpenPyXL** – Excel handling
* **NumPy** – Numerical processing
* **Pillow** – Image display in Tkinter

---

## 🔄 Project Flow

1. **Home Screen**

   * Navigate between “Register” and “Take Attendance” screens.

2. **Student Registration**

   * Enter Name and ID.
   * Capture 30 face images via webcam (grayscale).
   * Images are saved under `dataset/StudentName/`.
   * Data is stored in `students.xlsx`.

3. **Model Training**

   * After capturing, the model trains using LBPH algorithm.
   * A CSV file (`labels.csv`) stores label-name-ID mappings.
   * The model is saved in `trainer.yml`.

4. **Attendance Marking**

   * System activates webcam, scans for known faces.
   * If a face is recognized (with confidence < 70), attendance is marked for today’s date in the Excel sheet.

---


## 🚀 How to Run

1. Install required libraries:

```bash
pip install opencv-python opencv-contrib-python pandas openpyxl pillow
```

2. Run the app:

```bash
python main.py
```

Make sure your webcam is connected and working.

---


## 🎯 Use Case & Vision

This project was built as a practical implementation of **AI in education**. I plan to **showcase it to my school** with hopes of seeing it deployed in some classrooms as a trial initiative. With further refinement, it can reduce classroom administrative load and introduce students to real-world AI.

---

## 🙋‍♂️ Author

**Parantap Mishra**
Class 12, PCM with CS
Lotus Valley International School, Noida
👨‍💻 Passionate about AI, coding, and building real-world projects

