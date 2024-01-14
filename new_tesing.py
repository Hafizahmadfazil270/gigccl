import os
import cv2
from PIL import Image
import pytesseract as pt

# Assuming 'file_path' is the base directory
file_path = "media\myimages"
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

# List all files in the directory
all_files = os.listdir(file_path)

# Filter only files with image extensions
image_files = [
    f for f in all_files if any(f.lower().endswith(ext) for ext in image_extensions)
]

# Create full paths for image files
image_paths = [os.path.join(file_path, f) for f in image_files]

# Get the latest image based on modification time
latest_image_path = max(image_paths, key=os.path.getmtime, default=None)

if latest_image_path:
    print(f"The latest image is: {latest_image_path}")
    # Use the latest image path for further processing

    # Your existing code for processing the latest image
    def show_image(img_path, size=(500, 500)):
        image = cv2.imread(img_path)
        image = cv2.resize(image, size)
        cv2.imshow("IMAGE", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    pt.pytesseract.tesseract_cmd = r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

    img = Image.open(latest_image_path)
    text = pt.image_to_string(img)
    print("-----------------img text-------------------")
    print(latest_image_path)
    print(text)
    show_image(latest_image_path)

else:
    print("No image files found in the specified directory.")
