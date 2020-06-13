from PIL import Image

p = Image.open('1.png')
a,b = p.size
i = ''
count = 0
for y in range(b):
    for x in range(a):
        data = p.getpixel((x,y))[3]
        if data == 255:
            i+='1'
        else:
            i+='0'
a = open('all.txt','w')
a.write(i)
a.close()

data = open('all.txt','r').read()
block1 = Image.new('L',(10,10),0)
block2 = Image.new('L',(10,10),255)
res = Image.new('L',(330,330),0)
for i in range(33):
    for j in range(33):
        if data[j+33*i] == '1':
            res.paste(block1,(i*10,j*10))
        else:
            res.paste(block2, (i * 10, j * 10))
res.show()