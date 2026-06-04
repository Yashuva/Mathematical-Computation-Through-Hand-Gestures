# 🧮 Mathematical Computation Through Hand Gestures

## 📝 Overview

Mathematical Computation Through Hand Gestures is a computer vision-based application that allows users to perform mathematical calculations using hand gestures and air writing without requiring a keyboard or mouse.

The system uses a webcam to track hand movements, recognize gestures, interpret mathematical expressions, and calculate results in real time. It combines Computer Vision, Gesture Recognition, OCR, and Voice Output to create a touchless and interactive user experience.

---

## ✨ Features

### ✍️ Air Writing Mode

* Draw numbers and mathematical expressions in the air.
* OCR recognizes handwritten digits and operators.
* Automatically evaluates the expression.
* Displays the result in real time.

### ✋ Finger Gesture Math Mode

* Perform calculations using finger gestures.
* Recognize numbers through finger counting.
* Support arithmetic operators:

  * ➕ Addition
  * ➖ Subtraction
  * ✖ Multiplication
  * ➗ Division

### 🔊 Voice Output

* Reads the calculated result aloud.
* Improves accessibility and user interaction.

### 🎥 Real-Time Processing

* Live webcam feed.
* Instant gesture recognition.
* Immediate result display.

---

## 🛠 Technologies Used

* 🐍 Python
* 👁 OpenCV
* ✋ MediaPipe
* 🌐 Django
* 🔤 Tesseract OCR
* 🔢 NumPy
* 🔊 pyttsx3
* 🖼 Pillow
* 🎯 CVZone

---

## 📋 Requirements

* Python 3.10+
* Webcam
* Tesseract OCR Installed

Install required packages:

```bash
pip install -r requirements.txt
```

---

## 🚀 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/mathematical-computation-through-hand-gestures.git
```

### 2️⃣ Move to Project Directory

```bash
cd mathematical-computation-through-hand-gestures
```

### 3️⃣ Create Virtual Environment

```bash
python -m venv myenv
```

### 4️⃣ Activate Environment

Windows:

```bash
myenv\Scripts\activate
```

Mac/Linux:

```bash
source myenv/bin/activate
```

### 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 6️⃣ Install Tesseract OCR

Download and install Tesseract OCR.

Default Windows path:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

Configure pytesseract path inside the project if required.

### 7️⃣ Run Application

```bash
python manage.py runserver
```

Open browser:

```text
http://127.0.0.1:8000
```

---

## 🎮 How to Use

### ✍️ Air Writing Mode

* Raise index finger to draw.
* Write mathematical expressions in the air.
* Open hand gesture to solve the expression.
* Result will be displayed and spoken aloud.

### ✋ Finger Gesture Mode

* Show finger combinations to enter numbers.
* Use predefined gestures for operators.
* Expression is generated automatically.
* System calculates and displays the answer.

---

## 🔄 Project Workflow

Webcam Input
->
OpenCV Frame Processing
->
MediaPipe Hand Detection
->
Gesture Recognition / Air Writing
->
Tesseract OCR Processing
->
Expression Generation
->
Calculation Engine
->
Result Display & Voice Output

---

## 🎯 Applications

* Touchless Human-Computer Interaction
* Educational Learning Tools
* Smart Classrooms
* Accessibility Systems
* Interactive Mathematical Learning

---

## 🚀 Future Enhancements

* Scientific Calculator Support
* Advanced Mathematical Expressions
* Deep Learning-Based Gesture Recognition
* Mobile Application Version
* Multi-Hand Gesture Support

---



## 🙏 Acknowledgements

Special thanks to our project guide, faculty members, and teammates for their support and guidance throughout the development of this project.

---

## 📜 License

This project is developed for educational and academic purposes.
