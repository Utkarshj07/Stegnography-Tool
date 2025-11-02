from PIL import Image

def decode_text_from_image(image_path):
    """Extract hidden text from an encoded image."""
    img = Image.open(image_path)
    width, height = img.size
    binary_data = ""

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_data += str(r & 1)

    chars = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    decoded_text = ""

    for ch in chars:
        decoded_text += chr(int(ch, 2))
        if decoded_text.endswith("~~~~"):  # stop marker
            break

    return decoded_text.replace("~~~~", "")
