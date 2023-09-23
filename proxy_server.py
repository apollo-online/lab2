import socket
from threading import Thread


BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

# send client's request to destination server
def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: # initialize a new socket in with block to ensure it's closed once we're done
        client_socket.connect((host, port)) # connect socket to google host and port
        client_socket.send(request) # send request through the connected socket
        client_socket.shutdown(socket.SHUT_WR) # shut the socket to further writes, tell server we're done sending data
        
        # assemble response, be careful here, recall that recv(bytes) blocks until it recieves data
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0: # keep reading data until the connection terminates  
            data = client_socket.recv(BYTES_TO_READ)
            result += data

        return result # return response

# handle an incoming connection that has been accepted by the server
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b''
        while True: # while the client is keeping the socket open
            data = conn.recv(BYTES_TO_READ) # continously recieve any incoming data from the conn socket
            if not data: # if the socket has been closed to further writes, break (the client stopped sending data)
                break
            print(data)
            request += data
        response = send_request("www.google.com", 80, request) # forward client's request to google server
        conn.sendall(response) # return the response obtained from google server back to client

# Start multi threaded proxy server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: # initialize socket
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT)) # bind host and port to socket
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ignore for now
        server_socket.listen(2) # wait for connection on the socket that we bound with this server's host and port
        while True:
            conn, addr = server_socket.accept() # accept connection from client
            print("accepted request from client")
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

start_server()