from PIL import Image
import re
import pytesseract
import os

def invert_color(img_path) -> str:
    image = Image.open(img_path)
    # Invert the image
    inverted_image = Image.eval(image, lambda px: 255 - px)
    img_path.split('/')
    name, extension = os.path.splitext(img_path)
    new_name = name + '_inv'
    new_filename = new_name + extension
    # Save the inverted image
    inverted_image.save(f"{new_filename}")
    return new_filename


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_text(img_path) -> (float, str):
    inv_img_path = invert_color(img_path)
    data = pytesseract.image_to_string(Image.open(inv_img_path), lang='heb')
    if data == '':
        print("No Data Found")
        return False
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'
    dates = re.findall(date_pattern, data)

    price_pattern = r'לתשלום : (\d+\.\d{2})'
    prices = re.findall(price_pattern, data)
    for price in prices:
        print (float(price), dates[0])
    return float(prices[0]), dates[0]