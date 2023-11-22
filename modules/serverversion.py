from cryptography.fernet import Fernet
def main(message, ip, password, *args):
    if str(message) == "$server_version":
        text = "\nserver version is 3.0\n$changelog - to get changelog".encode()
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text)
        return f"client.send({text})"
    else:
        return "null"
