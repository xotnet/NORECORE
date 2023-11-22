from cryptography.fernet import Fernet
def main(message, ip, password, *args):
    if str(message) == "$changelog":
        text = "CHANGELOG v3.0\n[+] different types of crypt added (full message hidden crypt)\n[+] added connection notify\n[+] added messaging (based on box system)\n[+] added auto module init (just add file to modules path)\n[+] added client auto dissconect from server with connecion refused\n[/] fixed disconnect terminal flood \n[/] fixed ip showing in disconnect message \n[/] fixed bags"
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text.encode())
        return f'client.send({text})'
    else:
        return "null"
