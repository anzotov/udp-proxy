from socket import socket, SOCK_DGRAM
from time import sleep


def main():
    client_addr = ["192.168.0.10", 3333]
    client_socket = socket(type=SOCK_DGRAM)
    client_socket.setblocking(False)
    try:
        while True:
            inp = input().strip()
            if(inp):
                print(inp.encode())
                client_socket.sendto(inp.encode(), tuple(client_addr))
            try:
                data, addr = client_socket.recvfrom(4096)
                if data:
                    print(data)
            except:
                pass
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
