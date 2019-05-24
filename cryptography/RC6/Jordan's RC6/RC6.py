from helper import *

class RC6:
    def __init__(self):
        self.w = 32
        self.r = 12

    # takes in a string where it will convert it into encrypted text
    def encryption(self,message, s):
        cipher = []
        modulo = 2 ** 32
        lgw = 5
        encoded = toBlocks(message)
        original = []
        A = int(encoded[0], 2)
        original.append(A)
        B = int(encoded[1], 2)
        original.append(B)
        C = int(encoded[2], 2)
        original.append(C)
        D = int(encoded[3], 2)
        original.append(D)

        B = (B + s[0]) % modulo
        cipher.append(B)
        D = (D + s[1]) % modulo
        cipher.append(D)
        # the rounds we need to shift
        for i in range(1, r + 1):
            # gets the d/b register and get the mod it to 2^32
            ktemp = (D * (2 * D + 1)) % modulo
            ltemp = (B * (2 * B + 1)) % modulo
            # rotates the register value by 5
            u = rotateLeft(ktemp, lgw)
            t = rotateLeft(ltemp, lgw)
            # then we will use mod by 32
            tmod = t % 32
            umod = u % 32
            # rotate the xor register by the value of the mod
            A = (rotateLeft(A ^ t, umod) + s[2 * i]) % modulo
            C = (rotateLeft(C ^ u, tmod) + s[2 * i + 1]) % modulo
            (A, B, C, D) = (B, C, D, A)
        A = (A + s[2 * r + 2]) % modulo
        cipher.append(A)
        C = (C + s[2 * r + 3]) % modulo
        cipher.append(C)

        return original, cipher

    # takes in cypher text where it will convert it into a readable text
    def decryption(self,esentence, s):
        cipher = []
        modulo = 2 ** 32
        encoded = toBlocks(esentence)
        lgw = 5
        A = int(encoded[0], 2)
        cipher.append(A)
        B = int(encoded[1], 2)
        cipher.append(B)
        C = int(encoded[2], 2)
        cipher.append(C)
        D = int(encoded[3], 2)
        cipher.append(D)
        C = (C - s[2 * r + 3]) % modulo
        A = (A - s[2 * r + 2]) % modulo
        # the rounds we need to do the shifting
        for j in range(1, r + 1):
            i = r + 1 - j
            # swapping the register values
            (A, B, C, D) = (D, A, B, C)
            ktemp = (D * (2 * D + 1)) % modulo
            u = rotateLeft(ktemp, lgw)
            t_temp = (B * (2 * B + 1)) % modulo
            t = rotateLeft(t_temp, lgw)
            tmod = t % 32
            umod = u % 32
            C = (rotateRight((C - s[2 * i + 1]) % modulo, tmod) ^ u)
            A = (rotateRight((A - s[2 * i]) % modulo, umod) ^ t)
        D = (D - s[1]) % modulo
        B = (B - s[0]) % modulo
        orgi = []
        orgi.append(A)
        orgi.append(B)
        orgi.append(C)
        orgi.append(D)
        return cipher, orgi
