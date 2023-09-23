import socket

BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n" # we want to request host, google.com
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # STEP 1) use socket.socket() function to initialize client socket; AF_INET => IPV4, SOCK_STREAM => TCP
    s.connect((host, port)) # STEP 2) initiate connection with server (note it's a pair)
    s.send(request) # STEP 3) send request 
    s.shutdown(socket.SHUT_WR) # STEP 4) announce you are done sending request; SHUT_WR => stop writing on socket, otherwise server will keep waiting
    result = s.recv(BYTES_TO_READ) # STEP 5) continously recieve response from server
    while (len(result) > 0): # loop until there is no more incoming data
        print(result)
        result = s.recv(BYTES_TO_READ)

    s.close() # close client socket once finished; send b''

#get("www.google.com", 80) # we are requesting the given host via its port
get("localhost", 8080) # specified in our server file