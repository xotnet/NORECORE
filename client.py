import socket, threading, time
from threading import Thread
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

HOST = "0.0.0.0"
PORT = 1111
GottenSignal = 0
ServerAnswTimeOut = 0
pingsignal = 0
prefix = "Send message: "
ToUser = False
user = ""
password = ""

# creating and connection to socket block
socket = socket.socket()
try: socket.connect((HOST, PORT))
except:
    print("\n[ERROR] server connection error\n")
    exit()
#P2P communication block
def getanddecode():
    global GottenSignal, pingsignal, ToUser, user, prefix, password
    while True:
        message = socket.recv(1024).decode()
        if password != '':
            try:
                key = password.encode()
                f = Fernet(key)
                message = f.decrypt(message.encode())
                message = message.decode()
            except: 
                if pingsignal == 0: print(f"\n[CRYPT] ENCRYPT/DECRYPT FAILED")
        pingsignal = 0
        if str(message[:12]) == "passforcrypt":
            password = private_key.decrypt(bytes.fromhex(message[12:]), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
            print(f"\n[CRYPT] encryption key: ****{str(password.decode()[22:])}")
            password = str(password.decode())
            message = ""
        if str(message[:11]) == "chatstarted":
            print("\nYou in chat, type 'back' or 'home' to back")
            prefix = f"Send to ****{message[-4:]}: "
            user = message[11:]
            ToUser = True
        if str(message[:5]) == "Pong!":
            if password != '':
                try:
                    f = Fernet(password.encode())
                    message = f.encrypt(message.encode())
                    message = message.decode()
                except: print(f"\n[CRYPT] ENCRYPT/DECRYPT FAILED")
            socket.send(message.encode())
            pingsignal = 1
        if message != "" and message != "null"  and pingsignal == 0:
            print(message)
            GottenSignal = 1
def sendandencode():
    global GottenSignal, ToUser, ServerAnswTimeOut, prefix, user, exited, password
    while True:
        time.sleep(0.1)                        #100 milliseconds
        ServerAnswTimeOut += 1                 #add timeout waiting point
        if ServerAnswTimeOut == 36:            #check timeout (36 * 100 milliseconds = 3,6 sec)
            if pingsignal == 1: print("\nping is 3600+ milliseconds")
            else:
                print("\nserver's answer get time out (3600 milliseconds)")
                GottenSignal = 1
        if GottenSignal == 1:                  # main part of message sending
            message = input(f"\n{prefix}")
            if str(message) == "back" or str(message) == "home":
                prefix = "Send message: "
                ToUser = False
                user = ""
            if password != '':
                key = password.encode()
                f = Fernet(key)
                message = f.encrypt(message.encode())
                message = message.decode()
            if ToUser == False: socket.send(message.encode())
            else: socket.send(f"TU{user}{message}".encode())
            GottenSignal = 0
            ServerAnswTimeOut = 0
            if str(message) == "exit":
                socket.close()
                exit()
         
         
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()
private_key_hex = private_key.private_bytes(encoding=serialization.Encoding.DER, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()).hex()
public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo).hex()
socket.send(f"startcrypt{public_key_hex}".encode())

 
#init block
thread1 = Thread(target=getanddecode)
thread2 = Thread(target=sendandencode)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
