from PIL import Image

def encode_text_into_image(image_path, secret_text):
    """Hide secret text inside the image."""
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    data_index = 0
    binary_secret = ''.join(format(ord(i), '08b') for i in secret_text) + '1111111111111110'  # EOF marker

    for y in range(height):
        for x in range(width):
            if data_index < len(binary_secret):
                r, g, b = img.getpixel((x, y))
                r = (r & ~1) | int(binary_secret[data_index])
                encoded.putpixel((x, y), (r, g, b))
                data_index += 1

    return encoded
