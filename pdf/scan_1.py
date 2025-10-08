from PIL import Image, ImageOps, ImageFilter
import pytesseract

img = Image.open("1.jpg").convert("L")
img = img.resize((int(img.width*1.7), int(img.height*1.7)))
img = ImageOps.autocontrast(img)
img = img.filter(ImageFilter.MedianFilter(size=3))
text = pytesseract.image_to_string(img, lang="eng", config="--psm 6 --oem 1 -c preserve_interword_spaces=1")
print(text)
