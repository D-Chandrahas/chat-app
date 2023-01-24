import zmq
from time import time,sleep
import sqlite3


con = sqlite3.connect("main.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, contacts TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, message TEXT, time INTEGER)")
con.commit()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:3000")

print("Server started")

while True:
    type,part1,part2,part3 = socket.recv_multipart()

    type = type.decode()
    print(f"[{time()}] received {type} request")

    part1 = part1.decode()
    part2 = part2.decode()
    part3 = part3.decode()
    
    if(type == "msg"):
        cur.execute("INSERT INTO messages VALUES(NULL,?,?,?,?)",(part1,part2,part3,int(time())))
        con.commit()
        socket.send("True".encode())

    elif(type == "refresh"):
        res = cur.execute("SELECT sender,message FROM messages WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?) ORDER BY time ASC",(part1,part2,part2,part1))
        data = ""
        while((row := res.fetchone()) is not None):
            data += f"{row[0]},{row[1]}\n"
        socket.send(data.encode())

    elif(type == "contacts"):
        res = cur.execute("SELECT contacts FROM users WHERE username = ?",(part1,))
        contacts = res.fetchone()[0]
        socket.send(contacts.encode())

    elif(type == "login"):
        res = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?",(part1,part2))
        if(res.fetchone() is None):
            socket.send("False".encode())
        else:
            socket.send("True".encode())

    elif(type == "add"):
        res = cur.execute("SELECT * FROM users WHERE username = ?",(part2,))
        if(res.fetchone() is None):
            socket.send("False".encode())
        else:
            res = cur.execute("SELECT contacts FROM users WHERE username = ?",(part1,))
            contacts = res.fetchone()[0]
            contacts = contacts.splitlines()
            if(part2 in contacts):
                socket.send("Already".encode())
            else:
                cur.execute("UPDATE users SET contacts = contacts || ? WHERE username = ?",(part2 + "\n", part1))
                con.commit()
                res = cur.execute("SELECT contacts FROM users WHERE username = ?",(part2,))
                contacts = res.fetchone()[0]
                contacts = contacts.splitlines()
                if(part1 not in contacts):
                    cur.execute("UPDATE users SET contacts = contacts || ? WHERE username = ?",(part1 + "\n", part2))
                    con.commit()
                socket.send("True".encode())

    elif(type == "remove"):
        res = cur.execute("SELECT contacts FROM users WHERE username = ?",(part1,))
        contacts = res.fetchone()[0].splitlines()
        contacts.remove(part2)
        contacts = "\n".join(contacts)
        if(len(contacts) > 0):
            contacts += "\n"
        cur.execute("UPDATE users SET contacts = ? WHERE username = ?",(contacts,part1))
        con.commit()
        socket.send("True".encode())

    elif(type == "register"):
        res = cur.execute("SELECT * FROM users WHERE username = ?",(part1,))
        if(res.fetchone() is None):
            cur.execute("INSERT INTO users VALUES(NULL,?,?,?)",(part1,part2,""))
            con.commit()
            socket.send("True".encode())
        else:
            socket.send("False".encode())

    elif(type == "terminate"):
        socket.send("True".encode())
        break

    print(f"[{time()}] replied to {type} request")

    sleep(1)
print("Server terminated")
socket.close()