from cryptography.fernet import Fernet
import datetime
def main(message, ip, password, *args):
    if str(message) == "$time":
        text = str(datetime.datetime.now()).encode()
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text)
        return f"client.send({text})"
    else:
        return "null"
