# 🕵️‍♂️ StegnoVault - Image Steganography Tool

A modern PyQt5 desktop application to hide and extract text inside images using **LSB Steganography**.

---

## ✨ Features
- 🖼️ Hide text inside images (PNG/JPEG)
- 🔓 Extract hidden messages
- ⚙️ Simple PyQt5 GUI
- 💾 Saves encoded images as PNG (lossless)
- 🔐 Built with modular architecture (encode/decode/utils)

---

## 🧱 Folder Structure
StegnoVault/
├── encode.py → Contains GUI for encoding
├── decode.py → Contains GUI for decoding
├── utils → Contains core LSB steganography logic
├── main.py → Launch point for the app
└── assets → Icons and screenshots

---

Tech Stack
Python 3.x
PyQt5
Pillow (PIL)

---

## 🧩 Installation
```bash
git clone https://github.com/Utkarshj07/Stegnography-Tool.git
cd Stegnography-Tool
pip install -r requirements.txt
python main.py
