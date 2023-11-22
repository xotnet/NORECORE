def main(message):
    if str(message) == "logout" or str(message) == "$logout" or str(message) == "exit":
        return "disconnect"
    else:
        return "null"
