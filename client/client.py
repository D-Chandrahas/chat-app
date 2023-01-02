import zmq
import os
import json



CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
CONFIG = {
    "server": "tcp://127.0.0.1:5555",
    "username": None,
    "password": None
}

if os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        CONFIG = json.load(f)
else:
    with open(CONFIG_FILE, "w") as f:
        json.dump(CONFIG, f)

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(CONFIG["server"])

while(True):
    os.system("clear||cls")
    print("1. Login\n2. Register\n3. Settings\n4. Exit\n\nEnter option: ", end="")
    option = input()

    if option == "1":
        os.system("clear||cls")
        if CONFIG["username"] is None:
            username = input("Enter username: ")
            password = input("Enter password: ")
            if(username == "!back" or password == "!back"):
                continue
        else:
            username = CONFIG["username"]
            password = CONFIG["password"]
        print("\nPlease wait...")

        continue_loop = False

        while True:
            socket.send_multipart(("login".encode(),username.encode(),password.encode(),"None".encode()))
            valid_credentials = socket.recv().decode()
            if valid_credentials == "True":
                break
            print("Invalid credentials!\n")
            username = input("Enter username: ")
            password = input("Enter password: ")
            if(username == "!back" or password == "!back"):
                continue_loop = True
                break
            print("\nPlease wait...")

        if continue_loop: continue

        while True:
            print("please wait...")
            socket.send_multipart(("contacts".encode(),username.encode(),"None".encode(),"None".encode()))
            contacts = socket.recv().decode()
            contacts = contacts.splitlines()
            os.system("clear||cls")
            print("0. Back\n1. Add contact\n2. Remove contact\n3. Refresh contacts")
            for i,contact in enumerate(contacts):
                print(f"{i+4}. {contact}")
            print("\nEnter option: ", end="")
            option = input()
            if option.isdigit():
                option = int(option)
            else:
                input("\nInvalid option!\nPress enter to continue...")
                continue
            if option == 0:
                break
            elif option == 1:
                os.system("clear||cls")
                contact = input("Enter username: ")
                if(contact == "!back"): continue
                if(contact == username):
                    input("\nYou cannot add yourself!\nPress enter to continue...")
                    continue
                if(contact in contacts):
                    input("\nContact already added!\nPress enter to continue...")
                    continue
                socket.send_multipart(("add".encode(),username.encode(),contact.encode(),"None".encode()))
                exists = socket.recv().decode()
                if exists == "True":
                    contacts.append(contact)
                else:
                    input("\nUsername does not exist!\nPress enter to continue...")

            elif option == 2:
                os.system("clear||cls")
                print("Select contact to delete\n\n0. Cancel")
                for i,contact in enumerate(contacts):
                    print(f"{i+1}. {contact}")
                contact_index = input("\nEnter option: ")
                if contact_index.isdigit():
                    contact_index = int(contact_index)
                else:
                    input("\nInvalid option!\nPress enter to continue...")
                    continue

                if contact_index == 0:
                    continue

                elif contact_index > 0 and contact_index <= len(contacts):
                    contact = contacts[contact_index-1]
                    socket.send_multipart(("remove".encode(),username.encode(),contact.encode(),"None".encode()))
                    removed = socket.recv().decode()
                    if removed == "True":
                        contacts.pop(contact_index-1)
                        input("\nContact removed successfully!\nPress enter to continue...")
                    else :
                        input("\nFailed to remove contact!\nPress enter to continue...")

                else:
                    input("\nInvalid option!\nPress enter to continue...")

            elif option == 3:
                continue

            elif option > 3 and option <= len(contacts)+3:
                contact = contacts[option - 4]
                print("please wait...")

                while True:
                    #auto-refresh using another thread(?)
                    socket.send_multipart(("refresh".encode(),username.encode(),contact.encode(),"None".encode()))
                    conv = socket.recv().decode()
                    os.system("clear||cls")
                    for row in conv.splitlines():
                        sender, msg = row.split(",")
                        print(f"{sender}: {msg}")

                    msg = input(f"{username}: ")

                    if msg == "!back" or msg == "!b":
                        break

                    elif msg == "!refresh" or msg == "!r":
                        print("please wait...")
                        socket.send_multipart(("refresh".encode(),username.encode(),contact.encode(),"None".encode()))
                        conv = socket.recv().decode()
                        os.system("clear||cls")
                        for row in conv.splitlines():
                            sender, msg = row.split(",")
                            print(f"{sender}: {msg}")

                    else:
                        socket.send_multipart(("msg".encode(),username.encode(),contact.encode(),msg.encode()))
                        confirm = socket.recv().decode()
                        if confirm != "True":
                            input("Failed to send message!\nPress enter to continue...")

            else:
                input("\nInvalid option!\nPress enter to continue...")

    elif option == "2":
        while True:
            os.system("clear||cls")
            #20 char limit and no special characters(?)
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            if(username == "!back" or password == "!back"): break
            print("\nPlease wait...")
            socket.send_multipart(("register".encode(),username.encode(),password.encode(),"None".encode()))
            available = socket.recv().decode()
            if available == "True":
                print("\nRegistration successful!\n")
                while True:
                    save = input("Save username and password for quick login? (y/n): ")

                    if save == "y":
                        CONFIG["username"] = username
                        CONFIG["password"] = password
                        with open(CONFIG_FILE, "w") as f:
                            json.dump(CONFIG, f)
                        input("\nUsername and password saved successfully!\nPress Enter to continue...")
                        break

                    elif save == "n":
                        break

                    else:
                        print("Invalid option\n")

                break

            else :
                input("\nUsername not available!\nPress Enter to retry...")

    elif option == "3":
        while True:
            os.system("clear||cls")
            print("1. View saved credentials\n2. Change saved credentials\n3. Change server address\n4. Back\n\nEnter option: ", end="")
            option = input()

            if option == "1":
                os.system("clear||cls")
                with open(CONFIG_FILE, "r") as f:
                    loaded_config = json.load(f)
                if loaded_config["username"] is not None:
                    print(f'Username: {loaded_config["username"]}\nPassword: {loaded_config["password"]}')
                else:
                    print("No saved credentials found!")
                input("\nPress Enter to continue...")

            elif option == "2":
                os.system("clear||cls")
                username = input("Enter username: ")
                password = input("Enter password: ")
                if username == "!back" or password == "!back": continue
                else:
                    CONFIG["username"] = username
                    CONFIG["password"] = password
                with open(CONFIG_FILE, "w") as f:
                    json.dump(CONFIG,f)
                input("\nUsername and password saved successfully!\nPress Enter to continue...")
             
            elif option == "3":
                os.system("clear||cls")
                sev_addr = input("Enter new server address: ")
                if sev_addr == "!back": continue

                while True:
                    confirm = input("Confirm? (y/n): ")

                    if confirm == "y":
                        CONFIG["server"] = sev_addr
                        with open(CONFIG_FILE, "r") as f:
                            loaded_config = json.load(f)
                        loaded_config["server"] = sev_addr
                        with open(CONFIG_FILE, "w") as f:
                            json.dump(loaded_config, f)
                        input("\nServer address changed successfully!\nPress Enter to continue...")
                        break

                    elif confirm == "n":
                        input("\nServer address change cancelled!\nPress Enter to continue...")
                        break

                    else:
                        print("\nInvalid option\n")

            elif option == "4":
                break

            else:
                input("Invalid option...Press Enter to continue...")

    elif option == "4":
        os.system("clear||cls")
        break

    else:
        input("Invalid option...Press Enter to continue...")

socket.close()