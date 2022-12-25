import time
import zmq
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

os.system("clear||cls")

while True:
    type,recv_str = socket.recv_multipart()
    print(f"Received \"{recv_str.decode()}\" of type {type.decode()} from client")
    if recv_str == b"!back":
        break
    send_str = input("Server: ")
    print(f"Sent \"{send_str}\" to client")
    socket.send_multipart((b"msg",send_str.encode()))

socket.close()