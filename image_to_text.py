import os
import cv2
from PIL import Image
import pytesseract as pt

test_img_path = "media\myimages"
create_path = lambda f: os.path.join(test_img_path, f)
test_img_files = os.listdir(test_img_path)
for f in test_img_files:
    print(f)


def show_image(img_path, size=(500, 500)):
    image = cv2.imread(img_path)
    image = cv2.resize(image, size)
    cv2.imshow("IMAGE", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


pt.pytesseract.tesseract_cmd = r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

# show_img(test_img_files[0])
img_path = test_img_files[2]
path = create_path(img_path)
# print(path)
img = Image.open(path)
text = pt.image_to_string(img)
print("-----------------img text-------------------")
print(path)
print(text)
show_image(path)

image_path = test_img_files[12]  # 2, 3, 12, 1, 13, 15
path = create_path(image_path)

image = Image.open(path)
# text = pt.image_to_string(image, lang="eng")

print(image)
# show_image(path)
