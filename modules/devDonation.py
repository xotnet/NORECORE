def main(message, ip, password, *args):
    if str(message.lower()) == "$donate":
        text = "BitCoin donation: bc1q24sqqj6p6htuktap2vht2uzna9u7w3wlk8kfwk"
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text.encode())
        return f'client.send({text})'
    else:
        return "null"
