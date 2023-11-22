import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
symvols = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def main(message):
    password = ""
    for i in range(43):
        password = str(password) + symvols[random.randint(0, 61)]
    password = password + "="
    public_key = serialization.load_der_public_key(bytes.fromhex(message[10:]))
    message = password.encode()
    encrypted = public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return 'passforcrypt'.encode() + encrypted.hex().encode(), password
