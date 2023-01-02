import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")
socket.send_multipart(("terminate".encode(), "None".encode(), "None".encode(), "None".encode()))
print(socket.recv().decode())