
import binascii
import random
import string
import os
import ctypes

from coincurve import PrivateKey, PublicKey
from coincurve.utils import get_valid_secret
from Cryptodome.Cipher import AES

from eth_keys import keys
from eth_utils import decode_hex

AES_CIPHER_MODE = AES.MODE_GCM

__all__ = ["encrypt", "decrypt"]



# Convert a public key to hex
def hex2pub(pub_hex: str) -> PublicKey:
    uncompressed = decode_hex(pub_hex)
    if len(uncompressed) == 64:
        uncompressed = b"\x04" + uncompressed

    return PublicKey(uncompressed)

# Convert a private key  hex
def hex2prv(prv_hex: str) -> PrivateKey:
    return PrivateKey(decode_hex(prv_hex))


#Elliptic-curve Diffie–Hellman -> returns shared secret x.  
#https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman
def derive(private_key: PrivateKey, peer_public_key: PublicKey) -> bytes:
    return private_key.ecdh(peer_public_key.format())


#Encrypt a message using AES with shared secret. 
def aes_encrypt(key: bytes, plain_text: bytes) -> bytes:
    aes_cipher = AES.new(key, AES_CIPHER_MODE)
    encrypted, mac = aes_cipher.encrypt_and_digest(plain_text)
    cipher_text = bytearray()
    cipher_text.extend(aes_cipher.nonce)
    cipher_text.extend(mac)
    cipher_text.extend(encrypted)
    return bytes(cipher_text)


#Decrypt a message using AES with shared secret. 
def aes_decrypt(key: bytes, cipher_text: bytes) -> bytes:
    nonce = cipher_text[:16]
    mac = cipher_text[16:32]
    ciphered_data = cipher_text[32:]

    aes_cipher = AES.new(key, AES_CIPHER_MODE, nonce=nonce)
    return aes_cipher.decrypt_and_verify(ciphered_data, mac)



def generate_key() -> PrivateKey:
    return PrivateKey(get_valid_secret())


def generate_eth_key(secretString) -> keys.PrivateKey:
    return keys.PrivateKey(secretString)


def main():
    run = True
    secretString = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    
    #Generate receiver key's
    receiver_private_key = generate_eth_key(str.encode(secretString))
    receiver_private_KeyHex = receiver_private_key.to_hex()
    receiver_public_KeyHex = receiver_private_key.public_key.to_hex()
    receiver_aes_key = ""

    #Generate senders key pair
    senders_key = generate_key() 
    senders_aes_key = ""

    encrypted = ""

    #Prompt user to ask if they want to load their stored shared secret, or create a new one. 
    load_key_input = input("Load saved aes key?(y/n) ")

    #Check user input, and if there is a saved shared secret. 
    if(load_key_input =="y" and os.path.isfile('.supersecretfile')):
        f = open(".supersecretfile", "rb")
        receiver_aes_key = f.readline()
        senders_aes_key = receiver_aes_key
        print("Loaded aes key: " + str(receiver_aes_key))
    else:
        #ECDH -> save aes key for both sender and receiver 
        print("Executing Diffie–Hellman key exchange")
        receiver_aes_key = derive(hex2prv(receiver_private_KeyHex), senders_key.public_key) # Generate aes key from senders private key(a) and receiver's pubkey(B)
        print("Receiver -> get shared secret using my private key and senders public key")
        print("Shared secret: " + str(receiver_aes_key))
        senders_aes_key = derive(senders_key, hex2pub(receiver_public_KeyHex)) # Generate aes key from senders private key(a) and receiver's pubkey(B)
        print("Sender -> get shared secret using my private key and senders public key")
        print("Shared secret: " + str(senders_aes_key))


    while run:
        userInput = input("Please enter command: ")
        if(userInput == "encrypt"):
            message = input("Please enter message: ")
            encrypted = aes_encrypt(senders_aes_key, str.encode(message))
            print("Encrypted msg: " + str(encrypted))
        elif(userInput == "decrypt"):
            if(encrypted != ""):
                decrypted = aes_decrypt(receiver_aes_key, encrypted)
                print("Decrypted msg: " + str(decrypted))
            else:
                print("No encrypted message")
        elif(userInput == "savesecret"):
            #Src: https://stackoverflow.com/questions/25432139/python-cross-platform-hidden-file
            # For *nix add a '.' prefix.
            prefix = '.' if os.name != 'nt' else ''
            file_name = prefix + "supersecretfile"

            # Write bytes to file.
            with open(file_name, 'wb') as f:
                f.write(senders_aes_key)     
        elif(userInput == "help"):
            print("---- Available comands ----")
            print("encrypt -> To encrypt a message using ECC")
            print("decrypt -> To decrypt a message using ECC")
            print("savesecret -> Write aes key to hidden file")
            print("exit")
        elif(userInput == "exit"):
            run = False
        else:
            print("Invalid command")

        

main()


