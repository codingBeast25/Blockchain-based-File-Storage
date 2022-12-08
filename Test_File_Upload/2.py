import socket
import sys
import threading

BUFFER = 4096 #max size of a packet
HOST = '127.0.0.1'  #local host
PORT = 8800
#user prompt for display purpose
def user_prompt():
    print('>', end=' ',flush=True)

#recieves messages from server and displays it
def recieve():
    global flag
    while flag:
        try:
            mssg = server_socket.recv(BUFFER).decode()
            if mssg:
                if "Enter your name:" in mssg:
                    print(mssg)
                    user_name = input("")
                    server_socket.sendall(user_name.encode())
                else:
                    print(mssg)
                    user_prompt()
            else:
                break
        except:
            print("Error occurred while reciving from server!")
            break
#accpets input from user and send it to server            
def write():
    global flag
    while flag:
        try:
            mssg = input("")
            if '<quit>' in mssg:
                server_socket.sendall(mssg.encode())
            else:
                server_socket.sendall(mssg.encode())  
        except:
            print("Error occurred while sending to server!")
            break
                                
try:
    #flag to keep track if both threads are running ok
    flag = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.connect((HOST, PORT))#connect to server
    print('Connected to Chatsapp!\n')
    #create a thread for recieving data from server
    recieve_thr = threading.Thread(target = recieve)
    recieve_thr.start()
    #create thread for sending data to server
    send_thr = threading.Thread(target = write)
    send_thr.start()
    #if both threads still alive keep going and checking
    while recieve_thr.is_alive() and send_thr.is_alive():
        continue
    flag = False
    server_socket.close()
    print("\nDisconnected from server. Close the application by hitting Enter!")                                        
except KeyboardInterrupt:
    print("\nClient Disconnected!")
    sys.exit("Error")
                                         