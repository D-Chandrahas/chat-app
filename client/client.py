import time
import zmq
import os
import json


CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
CONFIG = {
    "server": "tcp://127.0.0.1:5555",
    "username": None,
    "password": None,
    "contacts": []
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
            CONFIG["username"] = input("Enter username: ")
            CONFIG["password"] = input("Enter password: ")
        print("\nPlease wait...")

        while True:
            socket.send_multipart(("login".encode(),CONFIG["username"].encode(),CONFIG["password"].encode(),"None".encode()))
            valid_credentials = socket.recv().decode()
            if valid_credentials == "True":
                break
            print("Invalid credentials!\n")
            CONFIG["username"] = input("Enter username: ")
            CONFIG["password"] = input("Enter password: ")
            print("\nPlease wait...")

        username = CONFIG["username"]
        while True:
            os.system("clear||cls")
            print("1. Back\n2. Add contact\n3. Remove contact")
            for i,contact in enumerate(CONFIG["contacts"]):
                print(f"{i+4}. {contact}")
            print("\nEnter option: ", end="")
            option = input()
            if option.isdigit():
                option = int(option)
            else:
                input("\nInvalid option!\nPress enter to continue...")
                continue
            if option == 1:
                break
            elif option == 2:
                os.system("clear||cls")
                contact = input("Enter username: ")
                socket.send_multipart(("contact".encode(),contact.encode(),"None".encode(),"None".encode()))
                exists = socket.recv().decode()
                if exists == "True":
                    CONFIG["contacts"].append(contact)
                    with open(CONFIG_FILE, "r") as f:
                        loaded_config = json.load(f)
                    loaded_config["contacts"].append(contact)
                    with open(CONFIG_FILE, "w") as f:
                        json.dump(loaded_config, f)
                else:
                    input("\nUsername does not exist!\nPress enter to continue...")

            elif option == 3:
                while True:
                    os.system("clear||cls")
                    print("Select contact to delete\n\n0. Cancel")
                    for i,contact in enumerate(CONFIG["contacts"]):
                        print(f"{i+1}. {contact}")
                    contact_index = input("\nEnter option: ")
                    if contact_index.isdigit():
                        contact_index = int(contact_index)
                    else:
                        input("\nInvalid option!\nPress enter to continue...")
                        continue

                    if contact_index == 0:
                        break

                    elif contact_index > 0 and contact_index <= len(CONFIG["contacts"]):
                        CONFIG["contacts"].pop(contact_index-1)
                        with open(CONFIG_FILE, "r") as f:
                            loaded_config = json.load(f)
                        loaded_config["contacts"].pop(contact_index-1)
                        with open(CONFIG_FILE, "w") as f:
                            json.dump(loaded_config, f)
                        input("\nContact removed successfully!\nPress enter to continue...")

                    else:
                        input("\nInvalid option!\nPress enter to continue...")

            elif option > 3 and option <= len(CONFIG["contacts"])+3:
                contact = CONFIG["contacts"][option - 4]
                socket.send_multipart(("refresh".encode(),username.encode(),contact.encode(),"None".encode()))
                conv = socket.recv() #placeholder
                #refresh and print screen
                while True:
                    #auto-refresh using another thread(?)
                    msg = input("You: ")

                    if msg == "!exit" :
                        break

                    elif msg == "!refresh" :
                        socket.send_multipart(("refresh".encode(),username.encode(),contact.encode(),"None".encode()))
                        conv = socket.recv().decode() #placeholder
                        #refresh and print screen

                    else:
                        socket.send_multipart(("msg".encode(),username.encode(),contact.encode(),msg.encode()))
                        confirm = socket.recv().decode()
                        if confirm != "True":
                            print("Failed to send message!")
                    print()

            else:
                input("\nInvalid option!\nPress enter to continue...")

            # while True:
            #     send_str = input("Client: ")
            #     socket.send_multipart((b"msg",send_str.encode()))
            #     if send_str == "!back":
            #         break
            #     type,recv_str = socket.recv_multipart()
            #     print(f"Received \"{recv_str.decode()}\" of type {type.decode()} from server")

    elif option == "2":
        while True:
            os.system("clear||cls")
            #20 char limit and no special characters(?)
            username = input("Enter new username: ")
            password = input("Enter new password: ")
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
                CONFIG["username"] = input("Enter username: ")
                CONFIG["password"] = input("Enter password: ")
                with open(CONFIG_FILE, "w") as f:
                    json.dump(CONFIG,f)
                input("\nUsername and password saved successfully!\nPress Enter to continue...")
             
            elif option == "3":
                os.system("clear||cls")
                sev_addr = input("Enter new server address: ")

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