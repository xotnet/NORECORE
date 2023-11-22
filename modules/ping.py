import datetime
import time
from datetime import datetime
from cryptography.fernet import Fernet
def main(message, ip, password, *args):
    if str(message) == "$ping":
        now = datetime.now()
        wstart = "%0.2d%0.2d" % (now.minute, now.second)
        text = f"Pong!{str(wstart)}".encode()
        if password != "":
            f = Fernet(password.encode())
            text = f.encrypt(text)
        return f'client.send({text})'
    elif str(message[:5]) == "Pong!":
        now = datetime.now()
        wstop = "%0.2d%0.2d" % (now.minute, now.second)
        wstart = str(message).replace("Pong!", ""); wstart = wstart.replace(":", "")
        if int(wstart):
            wstop = wstop.replace(":", "")
            ping = int(wstop) - int(wstart)
            if ping < 1:
                ret = str("\nping = ~0 second")
            else:
                ret = str("\n") + str(ping) + str(" seconds")
            text = str(ret).encode()
            if password != "":
                f = Fernet(password.encode())
                text = f.encrypt(text)
            return f"client.send({text})"
    else:
        return "null"
