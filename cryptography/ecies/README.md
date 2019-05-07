# Elliptic Curve Integrated Encryption Scheme (ECIES)

## What is a Elliptic Curve Integrated Encryption Scheme
Elliptic Curve Integrated Encryption Scheme, or ECIES, is a hybrid encryption system proposed by Victor Shoup in 2001. ECIES combines a Key Encapsulation Mechanism (KEM) with a Data Encapsulation Mechanism (DEM). The system independently derives a bulk encryption key and a MAC key from a common secret. Data is first encrypted under a symmetric cipher, and then the cipher text is MAC'd under an authentication scheme. Finally, the common secret is encrypted under the public part of a public/private key pair.


## How does ECC compare to RSA?
The biggest differentiator between ECC and RSA is key size compared to cryptographic strength.
  ![alt text](https://github.com/gudbrandsc/ECIES-project/blob/master/key-size-comparison.jpg "key size comparison")  
As you can see in the chart above, ECC is able to provide the same cryptographic strength as an RSA-based system with much smaller key sizes. For example, a 256 bit ECC key is equivalent to RSA 3072 bit keys (which are 50% longer than the 2048 bit keys commonly used today). The latest, most secure symmetric algorithms used by TLS (eg. AES) use at least 128 bit keys, so it makes sense that the asymmetric keys provide at least this level of security.


## Why would I want to use ECC?
The small key sizes make ECC very appealing for devices with limited storage or processing power, which are becoming increasingly common in the IoT. In terms of more traditional web server use cases, the smaller key sizes can offer speedier SSL handshakes (which can translate to faster page load times) and stronger security.
![alt text](https://github.com/gudbrandsc/ECIES-project/blob/master/Encryption-time-comparison-between-ECIES-and-RSA-AES.png "Encryption time comparison between ECIES and RSA")

## ecies.py
The goal for this script is to provide some easy understanding of how ECIES work. By creating two sets of key pairs (receiver and sender). By using (ECDH) we create a shared secret between the sender and receiver that allows them to communicate with each other without any eavesdropping third party being able to decrypt the messages. The user can also store their shared secret to a hidden file, and load the secret key the next time they run the script.

## Flow diagram 
 ![alt text](https://github.com/gudbrandsc/ECIES-project/blob/master/1_A3yiRaX7xBPBsovR_NyuVQ.png "ECIES flow diagram")

## Credit
https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman
https://www.cryptopp.com/wiki/Elliptic_Curve_Integrated_Encryption_Scheme
https://www.researchgate.net/publication/255970113_A_Survey_of_the_Elliptic_Curve_Integrated_Encryption_Scheme
https://medium.com/asecuritysite-when-bob-met-alice/generating-an-encryption-key-without-a-pass-phrase-meet-ecies-bbea1787d846
https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Secrecy_chart
https://www.globalsign.com/en/blog/elliptic-curve-cryptography/
https://github.com/ofek/coincurve
https://github.com/ethereum/eth-keys

