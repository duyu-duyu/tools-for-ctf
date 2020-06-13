msg=0x2559659965656a9a65656996696965a6695669a9695a699569666a5a6a6569666a59695a69aa696569666aa6
s=bin(msg)[2:]
r=""
for i in range(len(s)/2):
    if s[i*2:i*2+2] == '10':
        r += '1'
    else:
        r += '0'
print(hex(int(r,2))[2:-1].decode('hex'))