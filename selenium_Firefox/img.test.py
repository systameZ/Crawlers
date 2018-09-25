import pytesseract
from PIL import Image,ImageEnhance
im = Image.open("./img.jpg")
enhancer = ImageEnhance.Color(im.convert('RGB'))
enhancer = enhancer.enhance(0)
enhancer = ImageEnhance.Brightness(enhancer)
enhancer = enhancer.enhance(2)
enhancer = ImageEnhance.Contrast(enhancer)
enhancer = enhancer.enhance(8)
enhancer = ImageEnhance.Sharpness(enhancer)
im = enhancer.enhance(30)
#im=ImageEnhance.Sharpness(im).enhance(3)
vcode = pytesseract.image_to_string(im)
print(vcode)