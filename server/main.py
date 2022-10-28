import socket
import keyboard
from time import sleep
import configparser
import pygame


config = configparser.ConfigParser()

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#HOST = "192.168.0.136"
#PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
config.read('data/server.cfg')
HOST = config['HOST']['IP']
PORT = int(config['HOST']['PORT'])

print("Starting the server")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                pass
            else:
                stringdata = data.decode('utf-8')
                print(stringdata)
                if stringdata == "quit":
                    break
            conn.sendall(data)
