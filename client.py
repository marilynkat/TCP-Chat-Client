from os import system, name
import socket

# Static Variables
HOST = '10.0.0.1'
PORT = 65432

# Global variables
message_count = 0
messages = []
client_name = ""

# Function that clears the screen
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# Open a socket for TCP usage
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    
    # Connect to server with host and port provided above.
    sock.connect((HOST, PORT))

    # This loop handles all the sending and receiving of messages.
    while True:
        try:
            # Data being received, sent by server.
            recv_data = sock.recv(1024).decode()

            # If the server sent something.
            if recv_data:

                # If the server sent the Bye message close the application.
                if "Bye" in recv_data:
                    raise Exception()

                # This if statement allows me to manipulate a certain message so
                # that it looks good once it's printed out on the screen in the 
                # extra credit portion of the assignment.
                if ' received before ' in recv_data:
                    data_arr = recv_data.split(' received before ')
                    data1 = data_arr[0].split(': ')
                    data2 = data_arr[1].split(': ')
                    messages.append('Client ' + data1[0] + ' sent message 1: ' + data1[1] + '\n')
                    messages.append('Client ' + data2[0] + ' sent message 2: ' + data2[1])
                else:
                    # Add messages to a list
                    messages.append(recv_data)

                # If this is the first message we pull the name of the client
                # from it. It will either be 'X' or 'Y'.
                if message_count < 1:
                    client_name = recv_data.split()[1]
                
                # If the messafe count is less than 2 that means we haven't 
                # entered the extra credit section of the assignment so the 
                # output has to have a specific format.
                if message_count < 2:
                    print('From Server: ' + recv_data, end = '')

                # Once we reach more than 2 messages we enter extra credit mode
                # which enables the user to use the program as a proper chat client.
                # All of the chat history between the 2 clients is displayed.
                if message_count >= 2:
                    clear()
                    print('*********************************')
                    print('*       EXTRA CREDIT MODE       *')
                    print('*********************************')
                    for m in messages:
                        print(m, end = '')

                # User is prompted for message to be sent to the server and other client.
                message = input("Enter message to send to server: ")
                sock.sendall(message.encode())
                message_count += 1

        except:
            # The exception was written to close the chat client. An exception
            # is thrown on purpose if "Bye" is received to close down the client.
            print('\nTerminating Chat Client. Closing socket and exiting.')
            sock.close()
            exit()
