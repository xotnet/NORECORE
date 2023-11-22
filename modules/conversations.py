import os
from hashlib import sha256
from cryptography.fernet import Fernet
def main(message, ip, password, *args):
    if message == "$register" or message == "$reg" or message == "$id":
        idhash = sha256(ip.encode('utf-8')).hexdigest()
        try:
            f = open("./users.dat", "a+")
            if os.path.exists("./users.dat"):
                alldata = f.read()
                if f".{idhash}." not in alldata:
                    f.write(f".{idhash}.\n")
            f.close()
        except: pass
        text = f"\nYou successful registred, you id is: {idhash}".encode()
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text)
        return f'client.send({text})'
    elif str(message[:5]) == "$chat":
        if not os.path.exists("./box/"):
            os.mkdir("./box/")
        chatto = str(message[-64:])
        idhash = sha256(ip.encode('utf-8')).hexdigest()
        f = open("./users.dat", "r")
        alldata = f.read()
        f.close()
        if str(chatto) == str(idhash):
            text = "\nYou cant start chat with yourself".encode()
        else:
            if f".{chatto}." in alldata:
                text = f"chatstarted{chatto}".encode()
            else:
                text = "\nUser is not exists".encode()
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text)
        return f'client.send({text})'
    elif str(message[:2]) == "TU":
        userid = message[2:66]
        f = open("./users.dat", "r")
        alldata = f.read()
        f.close()
        if f".{userid}." in alldata and len(message) > 68:
            f = open(f"./box/{userid}", "a+")
            f.write(f"{sha256(ip.encode('utf-8')).hexdigest()}{message[66:]}\n")
            f.close()
            text = f"\nMessage sended. ****{userid[:-4]} get message in his box".encode()
        else:
            text = "User is not exists or message too low!".encode()
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text)
        return f"""client.send({text})"""
    elif str(message[:5]) == "$read":
        try:
            f = open(f"./box/{sha256(ip.encode('utf-8')).hexdigest()}", "r")
            msgs = f.read()
            f.close()
            msgs = msgs.splitlines()
            finmsg = "\nYour box:"
            for msg in msgs:
                if msg != "":
                    finmsg = finmsg + f"\n****{msg[60:64]}: {msg[64:]}"
            text = finmsg.encode()
            os.remove(f"./box/{sha256(ip.encode('utf-8')).hexdigest()}")
        except:
            text = f"\nYou dont have any message in your box".encode()
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text)
        return f'client.send({text})'
    elif str(message[:4]) == "back" or str(message[:4]) == "home":
        text = "Chat closed".encode()
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text)
        return f'client.send({text})'
    else:
        return "null"
