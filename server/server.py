import zmq
from time import time,sleep
import sqlite3


con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, message TEXT, time INTEGER)")
con.commit()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


while True:
    type,part1,part2,part3 = socket.recv_multipart()
    type = type.decode()
    part1 = part1.decode()
    part2 = part2.decode()
    part3 = part3.decode()
    if(type == "msg"):
        cur.execute("INSERT INTO messages(NULL,?,?,?,?)",(part1,part2,part3,int(time())))
        con.commit()
        socket.send("True".encode())
    elif(type == "refresh"):
        res = cur.execute("SELECT sender,message FROM messages WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?) ORDER BY time ASC",(part1,part2,part2,part1))
        data = ""
        while((row := res.fetchone()) is not None):
            data += f"{row[0]},{row[1]}\n"
        socket.send(data.encode())
    elif(type == "login"):
        res = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?",(part1,part2))
        if(res.fetchone() is None):
            socket.send("False".encode())
        else:
            socket.send("True".encode())
    elif(type == "contact"):
        res = cur.execute("SELECT * FROM users WHERE username = ?",(part1))
        if(res.fetchone() is None):
            socket.send("False".encode())
        else:
            socket.send("True".encode())
    elif(type == "register"):
        res = cur.execute("SELECT * FROM users WHERE username = ?",(part1))
        if(res.fetchone() is None):
            cur.execute("INSERT INTO users(NULL,?,?)",(part1,part2))
            con.commit()
            socket.send("True".encode())
        else:
            socket.send("False".encode())

    sleep(5)

socket.close()