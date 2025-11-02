# main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QGroupBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from stego_encode import encode_image
from stego_decode import decode_image
from PIL.ImageQt import ImageQt

class SteganographyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StegaVault - Image Steganography Tool")
        self.setGeometry(200, 100, 1000, 600)

        # ===== Left: Encode Section =====
        self.encode_group = QGroupBox("🔐 Encode Message")
        self.encode_layout = QVBoxLayout()

        self.encode_image_label = QLabel("No image selected")
        self.encode_image_label.setAlignment(Qt.AlignCenter)
        self.encode_image_label.setStyleSheet("border: 2px dashed #aaa; padding: 10px;")
        self.encode_button = QPushButton("Open Image (to encode)")
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
        self.encoded_image = None  # PIL Image
        self.decode_image_path = None

    # ========== ENCODE FUNCTIONS ==========
    def open_encode_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.encode_image_path = file_path
            pixmap = QPixmap(file_path).scaled(400, 250, Qt.KeepAspectRatio)
            self.encode_image_label.setPixmap(pixmap)

    def hide_text(self):
        if not self.encode_image_path:
            QMessageBox.warning(self, "Error", "Please select an image first.")
            return

        secret_text = self.text_box.toPlainText().strip()
        if not secret_text:
            QMessageBox.warning(self, "Error", "Please enter text to hide.")
            return

        try:
            self.encoded_image = encode_image(self.encode_image_path, secret_text)
        except Exception as e:
            QMessageBox.critical(self, "Encoding Error", f"Failed to encode: {e}")
            self.encoded_image = None
            return

        # preview encoded image in GUI
        qimage = ImageQt(self.encoded_image)
        pixmap = QPixmap.fromImage(qimage).scaled(400, 250, Qt.KeepAspectRatio)
        self.encode_image_label.setPixmap(pixmap)
        QMessageBox.information(self, "Success", "Text successfully hidden in image (preview shown). Now save it.")

    def save_encoded_image(self):
        if self.encoded_image:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Encoded Image", "", "PNG Image (*.png)")
            if save_path:
                # Ensure saving as PNG to avoid lossy compression
                if not save_path.lower().endswith('.png'):
                    save_path += '.png'
                self.encoded_image.save(save_path, "PNG")
                QMessageBox.information(self, "Saved", f"Encoded image saved: {save_path}")
        else:
            QMessageBox.warning(self, "Error", "No encoded image to save.")

    # ========== DECODE FUNCTIONS ==========
    def open_decode_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Encoded Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.decode_image_path = file_path
            pixmap = QPixmap(file_path).scaled(400, 250, Qt.KeepAspectRatio)
            self.decode_image_label.setPixmap(pixmap)

    def decode_text(self):
        if not self.decode_image_path:
            QMessageBox.warning(self, "Error", "Please select an encoded image first.")
            return

        try:
            message = decode_image(self.decode_image_path)
        except Exception as e:
            QMessageBox.critical(self, "Decoding Error", f"Failed to decode: {e}")
            return

        if message is None:
            QMessageBox.information(self, "Result", "No hidden text found (or sentinel missing).")
            self.decoded_text_box.setPlainText("")
        else:
            self.decoded_text_box.setPlainText(message)
            QMessageBox.information(self, "Decoded", "Hidden text successfully extracted!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteganographyApp()
    window.show()
    sys.exit(app.exec_())
