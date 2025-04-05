import socket  
import threading

from .log import Log
from .request import Request
from pathlib import Path

# Log instance
log = Log()

def handle_request(client_socket, client_address, file_directory):
    request = Request(client_socket.recv(2048), file_directory)
    server_answer = request.Request()
    log.info(f"client [{client_address[0]}:{client_address[1]}] accessing {request.request.base_path + '/' + request.request.rest_path} with method {request.request.method}")
    client_socket.sendall(server_answer)
    client_socket.close()

def main(file_directory):
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    log.debug("Server is active.")

    try:
        while True:
            client_socket, client_address = server_socket.accept() # wait for client
            log.info(f"Server accepted connection from the client [{client_address[0]}/{client_address[1]}]")
            if client_socket:
                threading.Thread(target=handle_request, args=(client_socket, client_address, file_directory)).start()

    except KeyboardInterrupt:
        log.debug("Server interrupted manually")

    except Exception as e:
        log.critical("Server closed due to an error, please verify the cause")
        print(e)

    finally:
        log.debug("Closing server")
        server_socket.close()



