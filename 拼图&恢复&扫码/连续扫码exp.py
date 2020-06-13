from rsav import *
from pyzbar.pyzbar import decode
from PIL import Image
bina=''
for i in range(1,577):
    image = 'QRcode\\'+str(i)+'.png'
    img = Image.open(image)
    barcodes = decode(img)
    for barcode in barcodes:
        url = barcode.data.decode("utf-8")
        bina+= '1' if url =='one' else '0'
print(bina)
flag = int(bina,2)
print(long_to_bytes(flag))
