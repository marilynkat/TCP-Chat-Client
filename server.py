# Multi-threading is necessary to run multiple clients concurrently with one server.
# This is so the server can communicate with both clients simultaneously without having
# to wait for other processes to finish. This enables faster communication between the 
# client and server. The threads generated are independent of each other so they can
# complete their designated task without interfering with each other. 

from _thread import start_new_thread
import threading, socket, os

# Static Variables
HOST = '10.0.0.1'
PORT = 65432

# Global variables
messages = []
clients = []
msg_count = 0
clients_lock = threading.Lock()

def main():
    global thread_count

    # Open a socket for TCP usage.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        # Listen for connections.
        sock.bind((HOST, PORT))
        sock.listen(2)

        print('The server is waiting to receive 2 connections...')

        try:
            # Accept 2 client connections to the server and start a thread
            # for each one of the connecting clients.
            while True:
                conn1, add = sock.accept()
                print('Accepted 1st connection, calling it client X')

                conn2, add = sock.accept()
                print('Accepted 2nd connection, calling it client Y')

                start_new_thread(threaded_client, (conn1, 'X'))
                start_new_thread(threaded_client, (conn2, 'Y'))

                print('\nWaiting to receive messages from client X and client Y...\n')
        except:
            print('exit')
    
def threaded_client(conn, client_name):
    global msg_count
    global messages
    global clients

    # Add client to a list so we can 
    # access them whenenever we need to.
    clients.append(conn)

    # First message is sent to the client stating their client name.
    connect_message = 'Client ' +  client_name + ' connected\n'
    conn.sendall(connect_message.encode())

    while True:

        # Receive data from the clients.
        try:
            recv_data = conn.recv(1024).decode()
        except:
            print("Connections Closed, Exiting!")
            exit()

        # If the server sent something.
        if not recv_data:
            break       
        else:
            # Increase the message counter.
            msg_count += 1

            # Print the message recived by the server that was sent by the client.
            message = 'Client ' + client_name + ' sent message ' + str(msg_count) + ': ' + recv_data + '\n'
            print(message[:-1])

            # Add messgae to a list of messages.
            messages.append((client_name, recv_data))

            with clients_lock:
                try:
                    # If the message list has 2 entries then we send a specific message to the
                    # clients stating which one sent the first message and which one sent the 
                    # second message.
                    if len(messages) == 2:
                        for c in clients:
                            response = (messages[0][0] + ': ' + messages[0][1] + ' received before ' + 
                                        messages[1][0] + ': ' + messages[1][1] + '\n')
                            c.sendall(response.encode())
                    
                    # If the message recived by the server is "Bye" we send a Bye
                    # to both servers telling them both to close. Then the connection
                    # is closed within this thread and the program is closed. 
                    if recv_data == "Bye":

                        for c in clients:
                            c.sendall(recv_data.encode())

                        print("Terminating chat.")
                        conn.close()
                        os._exit(1)

                    # If there's more than 2 messages in the list then we start sending 
                    # all of the incoming  messages back to both clients. This allows them
                    # to keep an accurate history of what's they're both sending and receiving.
                    if len(messages) > 2:
                        for c in clients:
                            c.sendall(message.encode())
                except:
                    print('Tried to receive message after one client had been closed.')

# Start program.
if __name__ == '__main__':
    main()
