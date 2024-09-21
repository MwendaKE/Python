import re
import sys
import os
import pytesseract
from pathlib import Path
from PIL import Image


# Use Pillow to open an image file

while True:
    print()
    image_path_input = str(input(" > Full path to image file: "))
    image_actual_path = Path(image_path_input)
    
    if re.match("Q|quit", image_path_input, re.I):
        print(" > Program exit !!")
        sys.exit(0)
        
    if not os.path.exists(image_actual_path):
        print(" > Path is invalid! Enter actual image path!")
        continue
        
    image = Image.open(image_actual_path)

    # Extract text from the image
    text = pytesseract.image_to_string(image)

    # Print the extracted text
    print()
    print("Extracted Text: \n")
    print("-" * 50)
    print(text)
    print("-" * 50)

'''
INSIGHT: To read text from an image using Python, 
you [can] use Optical Character Recognition (OCR). 
The most popular library for this task is Tesseract 
along with the Python wrapper Pytesseract.

With Tesseract and Pytesseract, you can easily 
extract text from images using Python. It works well 
for images with clear, high-contrast text, but for 
complex images, some preprocessing might be needed 
to improve accuracy.
'''