w = 32
r = 12

# by n bits
def rotateRight(n, d):
    return (n >> d) | (n << (w - d)) & 0xFFFFFFFF

# by n bits
def rotateLeft(x, n):
    return rotateRight( x, w - n)

# create private key from given input
def generateKey(input):
    modulo = 2 ** 32
    rounds = 2*r+4
    sArr = rounds * [0]
    sArr[0] = 0xB7E15163
    for i in range(1, rounds):
        sArr[i] = (sArr[i - 1] + 0x9E3779B9) % (2 ** w)
    encoded = toBlocks(input)
    encoLength = len(encoded)
    lArr = encoLength * [0]
    for i in range(1, encoLength + 1):
        lArr[encoLength - i] = int(encoded[i - 1], 2)

    v = 3 * max(encoLength, rounds)
    A = B = i = j = 0

    for index in range(0, v):
        A = sArr[i] = rotateLeft((sArr[i] + A + B) % modulo, 3)
        B = lArr[j] = rotateLeft((lArr[j] + A + B) % modulo, (A + B) % w)
        i = (i + 1) % rounds
        j = (j + 1) % encoLength
    return sArr

# converts input into binary blocks
def toBlocks(input):
    arr = []
    block = ""
    for i in range(0,len(input)):
        # helps create 4 blocks in 32 bits
        if i % 4 == 0 and i != 0:
            arr.append(block)
            block = ""
        temp = bin(ord(input[i]))[2:]
        if len(temp) <8:
            temp = "0"*(8-len(temp)) + temp
        block = block + temp
    arr.append(block)
    return arr

# converts blocks to a string
def unBlock(blocks):
    string = ""
    for element in blocks:
        temp = bin(element)[2:]
        if len(temp) < w:
            temp = "0" * (w - len(temp)) + temp
        for i in range(0, 4):
            string = string + chr(int(temp[i * 8:(i + 1) * 8], 2))
    return string
