# 🎯 Teachable Machine - Military Object Detection with Live UI (Pygame)

This project uses a trained TensorFlow model (from [Teachable Machine](https://teachablemachine.withgoogle.com/)) to perform **real-time object detection** of military units (e.g., missiles, tanks, jets) using your **webcam**. The results are displayed with a **custom UI built using Pygame**, with dynamic **highlighting** of the predicted class.

---

## 📦 Features

- ✅ Real-time webcam detection
- ✅ Supports `.h5` TensorFlow models exported from Teachable Machine
- ✅ Live UI with class boxes using Pygame
- ✅ Blinking green box around the predicted label
- ✅ Displays confidence score for each frame

---

## 🖥️ Classes Detected

```

0 - Missile
1 - Tanks
2 - Jets
3 - Drones
4 - B2 Bomber
5 - Nothing

```

---

## 📁 Files Required

- `keras_model.h5` → exported model from Teachable Machine
- `labels.txt` → exported class labels from Teachable Machine
- `run_model.py` → main Python script with OpenCV + Pygame UI

---

## 🧪 Requirements

Install Python packages:

```bash
pip install tensorflow opencv-python pygame numpy
```

You may also want to use a virtual environment:

```bash
# Create and activate environment (optional)
python -m venv TMenv
TMenv\Scripts\activate
```

---

## 🚀 How to Run

1. Make sure the following files are in the **same folder**:

   - `run_model.py`
   - `keras_model.h5`
   - `labels.txt`

2. Run the script:

```bash
python run_model.py
```

3. The webcam feed will open with the UI on the screen.

   - Detected class will blink green.
   - Press **`q`** or close the window to exit.

---

## 🛠️ Notes

- Built with:

  - TensorFlow 2.19+
  - OpenCV for webcam capture
  - Pygame for interactive UI

- The model was trained on Teachable Machine with 6 classes of military units.

---

## 📸 Preview

> _(Add a screenshot of your UI here if available)_

---

## 📄 License

This project is open-source and free to use for educational or research purposes.

---

## 👨‍💻 Author

**Manojkumar M**
_Internship Project – Real-time ML & UI with TensorFlow + Pygame_

```

---


```
