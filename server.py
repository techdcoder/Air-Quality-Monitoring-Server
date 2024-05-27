from socket import *
import threading
import select
import requests
import base64

wordpress_user = "arcallanamarco"
wordpress_password = "IWTGTJ2006AV0216"
wordpress_credentials = wordpress_user + ':' + wordpress_password
wordpress_token = base64.b64encode(wordpress_credentials.encode())
wordpress_header = {'Authorization': 'Basic ' + wordpress_token.decode('utf-8')}

def create_wordpress_post():
    api_url = 'https://f`indcoms024.wordpress.com/wp-json/wp/v2/posts'
    data = {
        'title': 'Example wordpress post',
        'status': 'publish',
        'slug': 'example-post',
        'content': 'This is the content of the post'
    }
    response = requests.post(api_url,headers=wordpress_header, json=data)
    print(response)


exit = False

def server_main(server_socket: socket):
    global exit
    while not exit:
        print("Server awaiting for connection")
        client_socket = None
        while not exit:
            read,_,_ = select.select([server_socket],[],[],0)
            if read:
                client_socket,_ = server_socket.accept()
                break
        print("Client Connected")
        while not exit:
            try:
                read,write,_ = select.select([client_socket],[client_socket],[], 0)
                if read:
                    data = client_socket.recv(1024)
                    if data[-1] == '\n':
                        data = data[:-1]
                    if data[-1] == '\r':
                        data = data[:-1]
                    mq2,mq5,mq7,temperature,humidity,pms1,pms2_5,pms10 = data.decode().split(',')
                    print(mq2,mq5,mq7,temperature,humidity,pms1,pms2_5,pms10)
                    if len(data) == 0:
                        print("Client disconnected")
                        break
            except select.error:
                print("Client disconnected")
                server_socket.close()
                break

def print_interface():
    print("Options: ")
    print("<1> Exit")
def main():
    global exit
    server_socket = socket(AF_INET, SOCK_STREAM)

    addr = ("192.168.1.33", 3600)

    server_socket.bind(addr)
    server_socket.listen(1)

    print("Server Initialized")
    server_thread = threading.Thread(target=server_main, args=[server_socket])

    server_thread.start()
    while True:
        print_interface()
        response = input("Input: ")

        if response == '1':
            exit = True
            break

    print("Terminating program, waiting for server socket to close")

    server_thread.join()
    server_socket.close()

    print("Server socket closed")


if __name__ == "__main__":
    main()