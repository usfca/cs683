from helper import *
import RC6
import sys


def mainEncrypt(rc6, key, sentence):
    if len(key) < 16:
        key = key + " " * (16 - len(key))
    key = key[:16]
    # get the key
    k = generateKey(key)
    print("Key:" + key)
    # limiting the size of the sentence to be 16
    if len(sentence) < 16:
        sentence = sentence + " " * (16 - len(sentence))
    sentence = sentence[:16]
    # returns the original text and cipher blocks
    orgi, cipher = rc6.encryption(sentence, k)
    # encrypts the cipher text that is in a binary block
    encrypted = unBlock(cipher)

    print("\nInput: " + sentence)
    print("Encrypted String: " + encrypted)

    f = open("encrypted.txt", "w")
    f.write(encrypted);
    f.close()
    return


def mainDecrypt(rc6, key):
    if len(key) < 16:
        key = key + " " * (16 - len(key))
    key = key[:16]

    print("Key: " + key)
    # get the key from provided string
    k = generateKey(key)
    f = open("encrypted.txt", "r")
    if not f:
        print("encrypted.txt not found")
        sys.exit(0)
    else:
        encrypted = f.readline()
    cipher, orgi = rc6.decryption(encrypted, k)
    sentence = unBlock(orgi)
    print("Encrypted String: " + encrypted)
    print("Decrypted String: " + sentence)

if __name__ == "__main__":
    args = sys.argv
    key = ""
    rc6 = RC6.RC6()
    for i in range(len(args)):
        if args[i] == "-key":
            key=args[i+1]
        if args[i] == "-encrypt":
            sentence = ""
            j = i+1
            for j in range(j,len(args)):
                sentence = sentence + " " + args[j]

            mainEncrypt(rc6, key, sentence)
        if args[i] == "-decrypt":
            mainDecrypt(rc6, key)
