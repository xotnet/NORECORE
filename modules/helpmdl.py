from cryptography.fernet import Fernet
def main(message, ip, password, *args):
    if str(message) == "help" or str(message) == "?" or str(message) == "$help":
        text = "\n$server_version - show server version\n$reg - get your user id\n$read - read your box\n$chat [user id] - join to chat\n$time - print server time\n$myip - show your ip\n$ping - check ping"
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text.encode())
        return f'client.send({text})'
    else:
        return "null"
