import random
import base64
import unittest

# finding gcd of two numbers


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Calculate the modular multiplicative inverse: such that d * e mod phi(n) = 1
def mulinverse(e, phi):
    d = 0
    x = 0
    y = 1
    z = 1
    temp = phi

    while e > 0:
        temp1 = temp/e
        temp2 = temp - temp1 * e
        temp = e
        e = temp2
        var1 = y - temp1 * x
        var2 = d - temp1 * z

        y = x
        x = var1
        d = z
        z = var2

    if temp == 1:
        return d + phi


# check whether the given intezer is prime or not
def checkprime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def keypair(p, q):

    """
     make sure user will not give same input, 2 numbers should be different. If not  exception will be raised
    """

    if not (checkprime(p) and checkprime(q)):
        raise ValueError('Please give (both) prime numbers as input.')
    elif p == q:
        raise ValueError('Please give distinct prime numbers')
    # using RSA algorithm
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    # Check whether they are coprimes or not
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # generate  private key
    d = mulinverse(e, phi)
    return ((e, n), (d, n))

# encrypting using key and n using m**e mod n formulae


def encrypting(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

# Decrypt using cipher, d, using c**d mod n formulae


def decrypting(pk, ciphertext):
    key, n = pk
    # using list comprehension to make it simple
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)


# 'unit test code to check whether the message which we sent using ecryption is same as received'


class TestMessage(unittest.TestCase):
    def test_message(self):
        self.assertEqual(message, result )
if __name__ == '__main__':
    p = int(raw_input("Enter a prime number (for more safety go with large values please): "))
    q = int(raw_input("Enter another prime number (ENter distinct values): "))
    publickey, privatekey = keypair(p, q)
    pub=base64.b64encode(bytes(str(publickey)))
    priv=base64.b64encode(bytes(str(privatekey)))
    message = raw_input("Enter a message which you want to be encrypted ")
    encrypted_msg = encrypting(privatekey, message)
    encipher= ''.join(map(lambda x: str(x), encrypted_msg))
    enc=base64.b64encode(bytes(str(encipher)))
    # initialise a dictionary
    dict = {}
    dict['public key'] = "-----BEGIN public KEY-----\n" + pub + "\n-----END public KEY-----\n" 
    dict['signature'] = enc
    dict['message'] = message
    result = decrypting(publickey, encrypted_msg)
    print dict
    # now test whether the the original message and decrpted message is equal or not using unittest
    unittest.main()
