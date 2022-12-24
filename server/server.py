import time
import zmq
import os

context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind("tcp://*:5555")

os.system("clear||cls")

while True:
    client_id,type,recv_str = socket.recv_multipart()
    print(f"Received \"{recv_str.decode()}\" of type {type.decode()} from {client_id}")
    if recv_str == b"!quit":
        break
    send_str = input("Server: ")
    print(f"Sent \"{send_str}\" to {client_id}")
    socket.send_multipart((client_id,b"msg",send_str.encode()))

socket.close()