import subprocess
import math
from tinytag import TinyTag
from torrentool.api import Torrent
import os
from fsplit.filesplit import Filesplit
from os import remove

#split_size-Split size in bytes

class Torrents(object):

	def __init__(self, archivo, port):

		#Fragmentar archivo
		fs = Filesplit()
		os.mkdir(str(archivo)+'fragmentado')
		fs.split(file=archivo, split_size=5000000, output_dir=str(archivo)+'fragmentado/')
		print("Su archivo "+str(archivo)+" ha sido fragmentado")

		remove(str(archivo)+"fragmentado/fs_manifest.csv")
		#Create torrent
		new_torrent = Torrent.create_from('/Users/HP-LAPTOP/Desktop/ProyectoSD/'+str(archivo)+'fragmentado')  
		new_torrent.announce_urls = 'udp://tracker.openbittorrent.com:'+str(port)+'/announce'
		new_torrent.to_file(str(archivo)+".torrent")

		







