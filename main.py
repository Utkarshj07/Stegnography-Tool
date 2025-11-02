import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QGroupBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image


class SteganographyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Steganography Tool")
        self.setGeometry(200, 100, 1000, 600)
        self.setStyleSheet("""
            QWidget { background-color: #f8f9fa; font-family: Segoe UI; }
            QPushButton { background-color: #0078d7; color: white; border-radius: 8px; padding: 8px; }
            QPushButton:hover { background-color: #005a9e; }
            QLabel { font-size: 12pt; }
            QTextEdit { border: 2px solid #ccc; border-radius: 8px; padding: 8px; }
        """)

        # ===== Left: Encode Section =====
        self.encode_group = QGroupBox("🔐 Encode Message")
        self.encode_layout = QVBoxLayout()

        self.encode_image_label = QLabel("No image selected")
        self.encode_image_label.setAlignment(Qt.AlignCenter)
        self.encode_image_label.setStyleSheet("border: 2px dashed #aaa; padding: 10px;")
        self.encode_button = QPushButton("Open Image")
        self.encode_button.clicked.connect(self.open_encode_image)

        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Enter text to hide...")

        self.hide_button = QPushButton("Hide Text in Image")
        self.hide_button.clicked.connect(self.hide_text)

        self.save_button = QPushButton("Save Encoded Image")
        self.save_button.clicked.connect(self.save_encoded_image)

        self.encode_layout.addWidget(self.encode_image_label)
        self.encode_layout.addWidget(self.encode_button)
        self.encode_layout.addWidget(self.text_box)
        self.encode_layout.addWidget(self.hide_button)
        self.encode_layout.addWidget(self.save_button)
        self.encode_group.setLayout(self.encode_layout)

        # ===== Right: Decode Section =====
        self.decode_group = QGroupBox("🔍 Decode Message")
        self.decode_layout = QVBoxLayout()

        self.decode_image_label = QLabel("No encoded image selected")
        self.decode_image_label.setAlignment(Qt.AlignCenter)
        self.decode_image_label.setStyleSheet("border: 2px dashed #aaa; padding: 10px;")
        self.decode_button = QPushButton("Open Encoded Image")
        self.decode_button.clicked.connect(self.open_decode_image)

        self.decoded_text_box = QTextEdit()
        self.decoded_text_box.setReadOnly(True)
        self.decoded_text_box.setPlaceholderText("Hidden text will appear here...")

        self.decode_text_button = QPushButton("Decode Hidden Text")
        self.decode_text_button.clicked.connect(self.decode_text)

        self.decode_layout.addWidget(self.decode_image_label)
        self.decode_layout.addWidget(self.decode_button)
        self.decode_layout.addWidget(self.decode_text_button)
        self.decode_layout.addWidget(self.decoded_text_box)
        self.decode_group.setLayout(self.decode_layout)

        # ===== Main Layout =====
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.encode_group)
        main_layout.addWidget(self.decode_group)
        self.setLayout(main_layout)

        # ===== Data Holders =====
        self.encode_image_path = None
        self.encoded_image = None
        self.decode_image_path = None

    # ========== ENCODE FUNCTIONS ==========
    def open_encode_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.encode_image_path = file_path
            pixmap = QPixmap(file_path).scaled(400, 250, Qt.KeepAspectRatio)
            self.encode_image_label.setPixmap(pixmap)

    def hide_text(self):
        if not self.encode_image_path:
            QMessageBox.warning(self, "Error", "Please select an image first.")
            return

        secret_text = self.text_box.toPlainText()
        if not secret_text:
            QMessageBox.warning(self, "Error", "Please enter text to hide.")
            return

        # Load the image
        img = Image.open(self.encode_image_path)
        encoded = img.copy()
        width, height = img.size
        data_index = 0
        binary_secret = ''.join(format(ord(i), '08b') for i in secret_text) + '1111111111111110'  # EOF marker

        for y in range(height):
            for x in range(width):
                if data_index < len(binary_secret):
                    r, g, b = img.getpixel((x, y))
                    r = (r & ~1) | int(binary_secret[data_index])  # modify LSB of red
                    encoded.putpixel((x, y), (r, g, b))
                    data_index += 1

        self.encoded_image = encoded
        QMessageBox.information(self, "Success", "Text successfully hidden in image!")

    def save_encoded_image(self):
        if self.encoded_image:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Encoded Image", "", "PNG Image (*.png)")
            if save_path:
                self.encoded_image.save(save_path, "PNG")
                QMessageBox.information(self, "Saved", "Encoded image saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "No encoded image to save.")

    # ========== DECODE FUNCTIONS ==========
    def open_decode_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Encoded Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.decode_image_path = file_path
            pixmap = QPixmap(file_path).scaled(400, 250, Qt.KeepAspectRatio)
            self.decode_image_label.setPixmap(pixmap)

    def decode_text(self):
        if not self.decode_image_path:
            QMessageBox.warning(self, "Error", "Please select an encoded image first.")
            return

        img = Image.open(self.decode_image_path)
        width, height = img.size
        binary_data = ""

        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                binary_data += str(r & 1)

        # Split into 8-bit chunks
        chars = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
        decoded_text = ""
        for ch in chars:
            decoded_char = chr(int(ch, 2))
            if decoded_text.endswith("~~~~"):  # detect end
                break
            decoded_text += decoded_char

        if decoded_text:
            # Remove EOF marker if present
            decoded_text = decoded_text.replace('~~~~', '')
            self.decoded_text_box.setPlainText(decoded_text)
            QMessageBox.information(self, "Decoded", "Hidden text successfully extracted!")
        else:
            QMessageBox.warning(self, "Error", "No hidden text found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteganographyApp()
    window.show()
    sys.exit(app.exec_())
