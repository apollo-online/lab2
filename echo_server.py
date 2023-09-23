import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1" # IP: localhost
PORT = 8080 # port clients will connect through

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True: # continously...
            data = conn.recv(BYTES_TO_READ) # recieve request from client
            if not data: # if b'' is recieved; client is done sending request
                break
            print(data) 
            conn.sendall(data) # echo the request

# Start single threaded echo server - redundant
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # STEP 1) initialize the socket; 'with' keyword automatically does s.close()
        s.bind((HOST,PORT)) # STEP 2) bind socket to hostname (ip) and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ignore for now
        s.listen() # STEP 3) listen to ip and port bound to socket for any incoming connections
        #print("waiting for connection")
        conn, addr = s.accept() # STEP 4) accept request from client; conn = socket referring to client, addr = ip and port of the client
        handle_connection(conn, addr) # handle request (see function)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr)) # create thread, each thread will handle a connection; send conn (socket ref) and address for each thread
            thread.run()

#start_server()
start_threaded_server()