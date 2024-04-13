from socket import socket, SOCK_DGRAM
from threading import Thread, Lock
from time import sleep


def main():
    client_addr = "192.168.0.10", 3333
    win_addr = "192.168.0.11", 3333
    win_wsl_addr = "172.18.224.1", 3334
    linux_wsl_addr = "172.18.234.41", 3333

    client_socket = socket(type=SOCK_DGRAM)
    wsl_socket = socket(type=SOCK_DGRAM)

    client_socket_lock = Lock()
    wsl_socket_lock = Lock()
    run_lock = Lock()
    run = True

    def client_handler():
        while True:
            data = b""
            addr = "", 0
            with client_socket_lock:
                try:
                    data, addr = client_socket.recvfrom(4096)
                except:
                    sleep(0.1)
            if data and addr[0] == client_addr[0]:
                with wsl_socket_lock:
                    wsl_socket.sendto(data, linux_wsl_addr)
            with run_lock:
                if not run:
                    break

    def wsl_handler():
        while True:
            data = b""
            addr = "", 0
            with wsl_socket_lock:
                try:
                    data, addr = wsl_socket.recvfrom(4096)
                except:
                    sleep(0.1)
            if data and addr == linux_wsl_addr:
                with client_socket_lock:
                    client_socket.sendto(data, client_addr)
            with run_lock:
                if not run:
                    break

    client_handler_thread = Thread(target=client_handler)
    wsl_handler_thread = Thread(target=wsl_handler)

    try:
        client_socket.setblocking(False)
        wsl_socket.setblocking(False)
        client_socket.bind(win_addr)
        wsl_socket.bind(win_wsl_addr)

        client_handler_thread.start()
        wsl_handler_thread.start()

        input("Press ENTER key to stop...")

    finally:
        run = False
        client_handler_thread.join()
        wsl_handler_thread.join()
        client_socket.close()
        wsl_socket.close()


if __name__ == "__main__":
    main()
