import zmq
import os
import json



CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
CONFIG = {
    "server": "tcp://127.0.0.1:3000",
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
    print("Main Menu\n\n0. Exit\n1. Login\n2. Register\n3. Settings\n\nEnter option: ", end="")
    option = input()

    if option == "0":
        os.system("clear||cls")
        break

    elif option == "1":
        os.system("clear||cls")
        print("Login\n")
        if CONFIG["username"] is None:
            username = input("Enter username: ")
            if username == "!b": continue
            password = input("Enter password: ")
            if password == "!b": continue
        else:
            username = CONFIG["username"]
            password = CONFIG["password"]
        print("\nPlease wait...")

        continue_loop = True

        while True:
            socket.send_multipart(("login".encode(),username.encode(),password.encode(),"None".encode()))
            valid_credentials = socket.recv().decode()
            if valid_credentials == "True":
                CONFIG["username"] = username
                CONFIG["password"] = password
                continue_loop = False
                break
            print("Invalid credentials!\n")
            username = input("Enter username: ")
            if username == "!b":
                break
            password = input("Enter password: ")
            if password == "!b":
                break
            print("\nPlease wait...")

        if continue_loop: continue

        while True:
            print("please wait...")
            socket.send_multipart(("contacts".encode(),username.encode(),"None".encode(),"None".encode()))
            contacts = socket.recv().decode()
            contacts = contacts.splitlines()
            os.system("clear||cls")
            print("Contacts\n\n0. Back\n1. Logout\n2. Add contact\n3. Remove contact\n4. Refresh contacts\n---------------------")
            for i,contact in enumerate(contacts):
                print(f"{i+5}. {contact}")
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
                CONFIG["username"] = None
                CONFIG["password"] = None
                break

            elif option == 2:
                os.system("clear||cls")
                print("Add contact\n")
                contact = input("Enter username: ")
                if(contact == "!b"): continue
                if(contact == username):
                    input("\nYou cannot add yourself!\nPress enter to continue...")
                    continue
                print("please wait...")
                socket.send_multipart(("add".encode(),username.encode(),contact.encode(),"None".encode()))
                exists = socket.recv().decode()
                if exists == "True":
                    contacts.append(contact)
                elif exists == "False":
                    input("\nUsername does not exist!\nPress enter to continue...")
                else:
                    input("\nContact already added!\nPress enter to continue...")

            elif option == 3:
                os.system("clear||cls")
                print("Select contact to delete\n\n0. Cancel\n--------------")
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

            elif option == 4:
                continue

            elif option > 4 and option <= len(contacts) + 4:
                contact = contacts[option - 5]
                print("please wait...")

                while True:
                    #auto-refresh using another thread(?)
                    socket.send_multipart(("refresh".encode(),username.encode(),contact.encode(),"None".encode()))
                    conv = socket.recv().decode()
                    os.system("clear||cls")
                    
                    for i, item in enumerate(conv.splitlines()):
                        print(f"{item}: ", end="") if i % 2 == 0 else print(f"{item}")

                    msg = input(f"{username}: ")

                    if msg == "!b":
                        break

                    elif msg == "!r":
                        pass

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
            print("Register\n")
            username = input("Enter new username: ")
            if username == "!b": break
            password = input("Enter new password: ")
            if password == "!b": break
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
            print("Settings\n\n0. Back\n1. View saved credentials\n2. Change saved credentials\n3. Delete saved credentials\n4. Change server address\n\nEnter option: ", end="")
            option = input()

            if option == "0":
                break

            elif option == "1":
                os.system("clear||cls")
                print("Saved credentials\n")
                with open(CONFIG_FILE, "r") as f:
                    loaded_config = json.load(f)
                if loaded_config["username"] is not None:
                    print(f'Username: {loaded_config["username"]}\nPassword: {loaded_config["password"]}')
                else:
                    print("No saved credentials found!")
                input("\nPress Enter to continue...")

            elif option == "2":
                os.system("clear||cls")
                print("Change saved credentials\n")
                username = input("Enter username: ")
                if username == "!b": continue
                password = input("Enter password: ")
                if password == "!b": continue
                with open(CONFIG_FILE, "r") as f:
                    loaded_config = json.load(f)
                loaded_config["username"] = username
                loaded_config["password"] = password
                with open(CONFIG_FILE, "w") as f:
                    json.dump(loaded_config, f)
                input("\nUsername and password saved successfully!\nRestart app for changes to take effect\nPress Enter to continue...")

            elif option == "3":
                os.system("clear||cls")
                print("Delete saved credentials?")
                while True:
                    confirm = input("Confirm? (y/n): ")

                    if confirm == "y":
                        with open(CONFIG_FILE, "r") as f:
                            loaded_config = json.load(f)
                        loaded_config["username"] = None
                        loaded_config["password"] = None
                        with open(CONFIG_FILE, "w") as f:
                            json.dump(loaded_config, f)
                        input("\nSaved credentials deleted successfully!\nPress Enter to continue...")
                        break

                    elif confirm == "n":
                        input("\nSaved credentials deletion cancelled!\nPress Enter to continue...")
                        break

                    else:
                        print("\nInvalid option\n")

            elif option == "4":
                os.system("clear||cls")
                print("Current server address:", CONFIG["server"])
                sev_addr = input("Enter new server address: ")
                if sev_addr == "!b": continue

                while True:
                    confirm = input("Confirm? (y/n): ")

                    if confirm == "y":
                        with open(CONFIG_FILE, "r") as f:
                            loaded_config = json.load(f)
                        loaded_config["server"] = sev_addr
                        with open(CONFIG_FILE, "w") as f:
                            json.dump(loaded_config, f)
                        input("\nServer address changed successfully!\nRestart app for changes to take effect\nPress Enter to continue...")
                        break

                    elif confirm == "n":
                        input("\nServer address change cancelled!\nPress Enter to continue...")
                        break

                    else:
                        print("\nInvalid option\n")

            else:
                input("Invalid option...Press Enter to continue...")

    else:
        input("Invalid option...Press Enter to continue...")

socket.close()