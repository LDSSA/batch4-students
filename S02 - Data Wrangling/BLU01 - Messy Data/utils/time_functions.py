from base64 import b64encode, b64decode


def f1():
    loops = int(b64decode(b'MTAwMA==').decode())
    count = 0
    for i in range(loops):
        count +=1


def f2():
    loops = int(b64decode(b'MDAxNQ==').decode())
    count = 0
    for i in range(loops):
        count +=1
