import io
import socket, threading, tqdm, os, sys, hashlib
import bencode 
from torrent import Torrents
from io import StringIO
from io import open
import subprocess

    
#from bitfield import Bitfield

username = input("Enter your username: ")

#Variables para el envio de archivos
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4 #4KB

host = '25.3.94.163'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

torre2="status.txt"

def enviar_file():
    cmd = ["python","Enviando.py"] 
    subprocess.run(cmd) 

def recibir_file():
    
    cmd = ["python","Recibiendo.py",str(torre2), "25.94.66.101"] 
    subprocess.run(cmd)


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
    
            else:
                f = open ('status.txt','a')
                f.write(message+"\n")
                f.close()      
        except:
            print("An error Ocurred")
            client.close
            break

def write_messages():
    respuesta=0
    while respuesta!="4":
        print("\n")
        print("****Introdusca un número segun sea su opción***")
        print("1.Dar de alta un archivo.")
        print("2.Descargar un archivo.")
        print("3.Ver lista de seguimiento.")
        print("4.Salir.")
        respuesta=input('')
        "*******************Compartiendo archivos*********************************"
        if respuesta=="1":
            print("Introdusca el nombre del archivo a compartir:")
            archivo=input('')
            Torrents(archivo,port)
            torre2=archivo
            respuesta="Compartiendo "+archivo
            message = f"{username}: {respuesta}"
            client.send(message.encode('utf-8'))
            f = open ('archivosTorrent.txt','a')
            f.write(str(username)+"|"+str(archivo)+".torrent"+"\n")
            f.close()
            enviar_thread.start()
        "*******************Descargando archivos*********************************"
        if respuesta=="2":

            print("Los archivos que tenemos disponibles son:")
            f = open ('archivosTorrent.txt','r')
            mensaje = f.read()
            print(mensaje)
            f.close()
            print("Ingrese el nombre del archivo que desea descargar")
            torre=input('')
            print("Leyendo archivo torrent...")
            torrent_file = open(torre, "rb") 
            metainfo = bencode.bdecode(torrent_file.read())
            info = metainfo['info'] 
            print ("Info: "+str(hashlib.sha1(bencode.bencode(info)).hexdigest()) )
            pieces = io.StringIO(str(info['pieces']))
            print ("Pieces: "+str(pieces) )
            recibir_thread.start()

        "*******************Viendo status de la red*********************************"
        if respuesta=="3":
            f = open ('status.txt','r')
            mensaje = f.read()
            print(mensaje)
            f.close()
            respuesta="Revisando de seguimiento"
            message = f"{username}: {respuesta}"
            client.send(message.encode('utf-8'))

        

    client.close()
        
    
        
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()

enviar_thread=threading.Thread(target=enviar_file)
recibir_thread=threading.Thread(target=recibir_file)




            