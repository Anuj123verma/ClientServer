from socket import *
import time
import sys
import socket
client_socket = socket.socket()
port = 6000
server_host = "192.168.56.65"
server_host_1="127.0.0.1"
server_host_2="192.168.52.41"
#taking input from the users for how many file to send
y = int(input("Enter number of files you want to send : "))
data=[]
for i in range(0,y):
    x = input()
    data.append(x)
client_socket.connect((server_host_1,port))
print("ready to send data")
index =0
next_frame_to_send=0;
frame_expected=0
ack_sent=1-frame_expected
packet_seq_no = next_frame_to_send
packet_ack_no = ack_sent
send_file=data[index]
fptr=open(send_file,'rb')
data_send=fptr.read(4096)
#making the packet for sending to the server
packet=str(packet_seq_no)+str(packet_ack_no)+str(len(send_file))+send_file+str(data_send)
#sending packet to the server
client_socket.sendall(packet.encode())
#setting the clock timer
#client_socket.settimeout(5000.0)
while(True):
    try:
        #recieving the ack from the server
        packet_recieved = client_socket.recv(1024).decode()
        if(int(packet_recieved[1])==next_frame_to_send):
            #client_socket.settimeout(0.0)
            #getting data from the file
            data_send = fptr.read(4096)
            next_frame_to_send = (next_frame_to_send+1)%2
        if(int(packet_recieved[0])==frame_expected):
            frame_expected = (frame_expected+1)%2
    except timeout:
        print("timeout")
    data_send=str(data_send)
    if(data_send!="b''"): #for noempty
        packet=str(next_frame_to_send)+str(1-frame_expected)+(data_send) 
        # sending packet to the server 
        client_socket.sendall(packet.encode())
    if(data_send=="b''"):
        index=index+1
        if(index>=y):
            print("File Transferred Succesfully!!!")
            packet=data_send
            #sending packet to the server
            client_socket.sendall(packet.encode())
            daka=client_socket.recv(1024).decode()
            print(daka)
            break
        send_file=data[index]
        fptr=open(send_file,'rb')
        data_send = str(fptr.read(4096))
        packet=str(next_frame_to_send)+str(1-frame_expected)+str(len(data[index]))+data[index]+(data_send)
        #sending packet to the server
        client_socket.sendall(packet.encode())
    #client_socket.settimeout(5000.0)    
client_socket.close()

    
        
        



        

        
        
           
        
