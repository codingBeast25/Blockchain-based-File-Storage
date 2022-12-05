# Name: Bhautik Sojitra
# Course: COMP 4300
# Assignment #1
# Purpose: Multi threaded Web chat application using python sockets



import threading
import socket
from time import sleep


# creating socket connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect(('127.0.0.1', 59000))


#  receives message from server and prints it on client console
def client_receive():

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
            
        except:
            print('Error in client_receive function !')
            client.close()
            break
            


# basically sends the client commands to users to process
def client_send():
    while True:
        try:
            sleep(0.01)
            message = input(">>> ")
            client.send(message.encode('utf-8'))
        except KeyboardInterrupt as k:
            print("Key board Interrupt ...")
            break
        except Exception as e:
            print(" Unknown Exception occured ! ...")
            break
        
            
            
        
# assigning an unique nickname to the client
message = client.recv(1024).decode('utf-8')
user_name = ''
while message != "SUCCESS":
    print(message)
    user_name = input("")
    client.send(user_name.encode('utf-8'))
    message = client.recv(1024).decode('utf-8')
    
     

#  initiating receive thread
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

client_send()


client.close()
