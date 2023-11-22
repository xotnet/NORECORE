from cryptography.fernet import Fernet
def main(message, ip, password, *args):
    if str(message) == "$myip":
        text = f"your ip is: {ip}"
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text.encode())
        return f'client.send({text})'
    else:
        return "null"
