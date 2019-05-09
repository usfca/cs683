# Program for encrypting files using pynacl, Omar Sharif, CS 683
# This class will be used to create Unix executable programs that will take
# predetermined keys to encrypt and predetermined keys to decrypt

import nacl.utils
from nacl.public import PrivateKey, Box, PublicKey
import json
from pathlib import Path

'''
Program that uses public key cryptography to encrypt all text files in a directory using PyNaCl library. Private and Public keys are persisted using json.
'''


class Pynacl:
    def __init__(self):
        pass

    def generate_keys(self):
        # Generate first users public and private keys
        # Public key is generated using Curve25519 high-speed elliptic curve cryptography
        private_key1 = PrivateKey.generate()
        public_key1 = private_key1.public_key
        p1 = str(private_key1)
        p2 = str(public_key1)

        # Generate second users public and private keys, after this public keys between users should be exchanged
        private_key2 = PrivateKey.generate()
        public_key2 = private_key2.public_key
        p3 = str(private_key2)
        p4 = str(public_key2)

        with open('config.json') as json_file:
            data = json.load(json_file)
            data['private_key1'] = p1
            data['public_key1'] = p2
            data['private_key2'] = p3
            data['public_key2'] = p4
        json_file.close()
        print("New public and private keys generated:")
        print(p1)
        print(p2)
        print(p3)
        print(p4)
        print()

        with open("config.json", "w") as json_file2:
            json.dump(data, json_file2, indent=4, sort_keys=True)
        json_file2.close()

    def encrypt(self, file):
        private_key1 = PrivateKey(b"iWxAD\xf6\xe4?r\xa1\xed\x1e\xf0'\xcc\x02\xb5o\x0e\xc8^o\x8f\xccE\xe1\x05b\xf9\xa11+")
        public_key2 = PublicKey(b'\xe6I`\x16\xe7bT\xab\xba+\xd2\xbe\x1f`\xab%n\xe2\xc3\xb9<n\x82\xcb\xd4\xfa\xdc\xf8L=`Z')

        # Read in contents of file, encrypt them, then write back
        with open(file) as f:
            content = f.read()
        f.close()
        bytesData = content.encode()

        user_box1 = Box(private_key1, public_key2)
        nonce = nacl.utils.random(Box.NONCE_SIZE)
        encrypted = user_box1.encrypt(bytesData, nonce)

        with open(file, "w") as text_file:
            text_file.write(str(encrypted))
        text_file.close()

    def decrypt(self, file):
        # read encrypted data from file
        with open(file) as f:
            content = f.read()
        f.close()
        content2 = self.str_to_bytestring(content)

        # decrypt encrypted data and write back to file
        private_key2 = PrivateKey(b'#"\xbf.\xe1[\xdd\x95\xe0s\xb7\xd8\xb5\xe3\xe3\x1e\xa1\x1c\xf7r\xec\xa3\\\xda\x7f4\x9cy\r7\xffJ')
        public_key1 = PublicKey(b"\xe6\xd2\xd1\x94\xde\x00s\xcew\xf1\xfc\x1a;\xacB]rqzu\xe8\rr\x19\x19p'\xbe\xe6z\xba ")
        user_box2 = Box(private_key2, public_key1)
        decrypted = user_box2.decrypt(content2).decode("utf-8")

        with open(file, "w") as text_file:
            text_file.write(decrypted)
        text_file.close()

    '''
    This function takes a string representing a byte array (usually a key or encrypted data read from a file) and turns it into an actual byte string.
    '''
    def str_to_bytestring(self, string):
        string = string[2:]
        string = string[:-1]

        bytes = string.encode()
        bytes2 = bytes.decode('unicode-escape').encode('ISO-8859-1')

        return bytes2

    def iterate_encrypt(self, directory):
        pathlist = Path(directory).glob('**/*.txt')
        for path in pathlist:
            # because path is object not string
            path_in_str = str(path)
            print(path_in_str)
            self.encrypt(path_in_str)
        print("All files successfully encrypted. \n")

    def iterate_decrypt(self, directory):
        pathlist = Path(directory).glob('**/*.txt')
        for path in pathlist:
            # because path is object not string
            path_in_str = str(path)
            print(path_in_str)
            self.decrypt(path_in_str)
        print("All files successfully decrypted. \n")


def main():
    pynacl = Pynacl()
    directory = "/Users" # enter this project directory here
    #pynacl.iterate_encrypt(directory)
    pynacl.iterate_decrypt(directory)


if __name__ == "__main__":
    main()