import time
import zmq
import os


CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")
SERVER_ADDRESS = "tcp://127.0.0.1:5555"
USERNAME = None
PASSWORD = None

if os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        lines = f.read().splitlines()
        if len(lines) == 3:
            SERVER_ADDRESS,USERNAME,PASSWORD = lines
        else:
            SERVER_ADDRESS = lines[0]
else:
    with open(CONFIG_FILE, "w") as f:
        f.write(SERVER_ADDRESS)

while(True):
    os.system("clear||cls")
    print("1. Login\n2. Register\n3. Settings\n4. Quit\n\nEnter option: ", end="")
    option = input()

    if option == "1":
        os.system("clear||cls")
        if USERNAME is None or PASSWORD is None:
            USERNAME = input("Enter username: ")
            PASSWORD = input("Enter password: ")
        print("\nPlease wait...")
        valid_credentials = False
        while True:
            #check and login and set valid_credentials
            valid_credentials = True
            if valid_credentials:
                break
            print("Invalid credentials!\n")
            USERNAME = input("Enter username: ")
            PASSWORD = input("Enter password: ")
            print("\nPlease wait...")
        os.system("clear||cls")
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        socket.connect(SERVER_ADDRESS)
        while True:
            send_str = input("Client: ")
            socket.send_multipart((b"msg",send_str.encode()))
            if send_str == "!quit":
                break
            type,recv_str = socket.recv_multipart()
            print(f"Received \"{recv_str.decode()}\" of type {type.decode()} from server,")
        socket.close()
    elif option == "2":
        while True:
            os.system("clear||cls")
            #20 char limit and no special characters
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            print("\nPlease wait...")
            #check and register and set available
            available = True
            if available:
                USERNAME = username
                PASSWORD = password
                print("\nRegistration successful!\n")
                while True:
                    save = input("Save username and password for quick login? (y/n): ")
                    if save == "y":
                        with open(CONFIG_FILE, "w") as f:
                            f.write(SERVER_ADDRESS + "\n" + USERNAME + "\n" + PASSWORD)
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
                    lines = f.read().splitlines()
                if len(lines) == 3:
                    print("Username: " + lines[1] + "\nPassword: " + lines[2])
                    input("\nPress Enter to continue...")
                else:
                    print("No saved credentials found!")
                    input("\nPress Enter to continue...")

            elif option == "2":
                os.system("clear||cls")
                username = input("Enter username: ")
                password = input("Enter password: ")
                USERNAME = username
                PASSWORD = password
                with open(CONFIG_FILE, "w") as f:
                    f.write(SERVER_ADDRESS + "\n" + USERNAME + "\n" + PASSWORD)
                input("\nUsername and password saved successfully!\nPress Enter to continue...")
             
            elif option == "3":
                os.system("clear||cls")
                sev_addr = input("Enter new server address: ")
                while True:
                    confirm = input("Confirm? (y/n): ")

                    if confirm == "y":
                        SERVER_ADDRESS = sev_addr
                        if USERNAME is None or PASSWORD is None:
                            with open(CONFIG_FILE, "w") as f:
                                f.write(SERVER_ADDRESS)
                        else:
                            with open(CONFIG_FILE, "w") as f:
                                f.write(SERVER_ADDRESS + "\n" + USERNAME + "\n" + PASSWORD)
                        input("\nServer address changed successfully!\nPress Enter to continue...")
                        break
                    elif confirm == "n":
                        input("\nServer address change cancelled!\nPress Enter to continue...")
                        break
                    else:
                        print("\nInvalid option")

            elif option == "4":
                break
            else:
                input("Invalid option...Press Enter to continue...")

    elif option == "4":
        os.system("clear||cls")
        break
    else:
        input("Invalid option...Press Enter to continue...")