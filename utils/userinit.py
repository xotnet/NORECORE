from hashlib import sha256
import os
def main(client, ip):
    notifystat = "Notifications not found"
    #check notifications
    id = sha256(ip.encode('utf-8')).hexdigest()
    if os.path.exists(f"./box/{id}"):
        notifystat = "!!!Someone sent you a message!!!"
    return f"\n[INFO] welcome from server, to get command list type: help or ?\n\n{notifystat}".encode()
