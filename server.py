import socket
import importlib.machinery
import importlib.util
import asyncio
import requests
from threading import Thread
from hashlib import sha256
from utils import notnullmessagecheckmdl, logout, userinit, crypt
from cryptography.fernet import Fernet
import os

HOST = "0.0.0.0"
PORT = 1111
PACKAGE_SIZE = 1024
password = ""
modulelist = []
notcommandword = []

#socket start block
socket = socket.socket()
socket.bind((HOST, PORT))
socket.listen()
socket.setblocking(False)

#auto update check
def enableautoupdatecheck():
    prfx = "[Updater] "
    try:
        if os.path.exists("AutoUpdate.dat"):
            f = open("AutoUpdate.dat", "r")
            au = f.read(1)
            if au == "y":
                print(f"{prfx}Checking for update...")
                response = requests.get("https://codeberg.org/avut0l6m/NORE-CORE/raw/branch/main/repodata/version")
                aus = f.read()
                if str(aus) != "":
                    if str(response.text) != str(aus[1:]):
                        print(f"{prfx}Update found! Download it on https://codeberg.org/avut0l6m/NORE-CORE\n")
                    else:
                        print(f"\n{prfx}Update not found\n")
                else:
                    u = open("AutoUpdate.dat", "w+")
                    u.write(f"y\n{response.text}")
                    u.close()
                    print(f"\n{prfx}Update not found")
            f.close()
        else:
            enableautoupdate = input("Enable auto update [y] / [n]: ")
            if str(enableautoupdate) == "y" or str(enableautoupdate) == "\n":
                f = open("AutoUpdate.dat", "a+")
                f.write("y")
                f.close()
                enableautoupdatecheck()
            else:
                f = open("AutoUpdate.dat", "a+")
                f.write("n")
                f.close()
    except Exception as e:
        print(f"\nError with update check ({e})\n")
enableautoupdatecheck()

print("Server started\n")

#modules import block | help, server_version...
                                        #TO CREATE YOUR OWN MODULE (command and more, handler) CREATE FILE IN MODULES PATH AND PUT
                                        #THERE MAIN DEF, IN MAIN DEF(message, ip) SET SCRIPT INCLUDE IF, ELSE, THEN, helpmdl.py - not full example
for fileses in os.walk("modules/"):
	for files in fileses:
		for mdl in files:
		    if mdl[-3:] == ".py":
		        modulelist.append(mdl[:-3])

#client init block
async def getdata(client):
    password = ""
    cryptexchange = 0
    loop = asyncio.get_event_loop()
    try:
        while True:
            message = ((await loop.sock_recv(client, PACKAGE_SIZE)).decode()) # seting message
            if str(message[:10]) == "startcrypt":
                ret, password = crypt.main(message)
                client.send(ret)
            if password != "":
                f = Fernet(password.encode())
                try: message = f.decrypt(message.encode()).decode()
                except: pass
                cryptexchange += 1
            ip = client.getpeername()[0]
            server_give_aswer = False

            #------------------------------------------------------- #MODULES -----------------------------------------------------------------#
            for mdl in modulelist:
                loader = importlib.machinery.SourceFileLoader(mdl, f'modules/{mdl}.py')
                spec = importlib.util.spec_from_loader(mdl, loader)
                module = importlib.util.module_from_spec(spec)
                loader.exec_module(module)
                
                returned = module.main(message, client.getpeername()[0], password)
                if returned != "null":
                    exec(returned)
                    server_give_aswer = True
                
            if not server_give_aswer and cryptexchange == 2:
                unkc = "\nunknown command! type help\nor ? to get command list"
                if password != "":
                    f = Fernet(password.encode())
                    unkc = f.encrypt(unkc.encode()).decode()
                client.send(unkc.encode())                 # unknown command module
            #----------------------------------------------------- #ENDMODULES ----------------------------------------------------------------#
            
            #CHECKS
            returned = notnullmessagecheckmdl.main(message)
            disconnected = False
            if returned != "null":
                client.close()
                disconnected = True
            if disconnected != True and message[:2] != "TU":
                if message[:10] == "startcrypt": client_message = f"[****{sha256(client.getpeername()[0].encode('utf-8')).hexdigest()[60:64]}] " + "crypt key exchange ended (" + message[160:200] + ")"
                else: client_message = f"[****{sha256(client.getpeername()[0].encode('utf-8')).hexdigest()[60:64]}] " + message
                print(client_message)
            returned = logout.main(message)
            if returned == "disconnect": client.close()
        client.close()
    except:
        try: print(f"[****{sha256(ip.encode('utf-8')).hexdigest()[60:64]}] Client disconnected")
        except: pass

#init block
async def client_init():                #client init and send welcome message
    global client
    loop = asyncio.get_event_loop()
    while True:
        try:
            client, add = await loop.sock_accept(socket)  # client connection
            returned = userinit.main(client, client.getpeername()[0])
            client.send(returned)  # welcome message
            loop.create_task(getdata(client))
            print(f"[****{sha256(client.getpeername()[0].encode('utf-8')).hexdigest()[60:64]}] connected")
        except: pass

asyncio.run(client_init())
