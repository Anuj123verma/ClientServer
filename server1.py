import socket
import sys
import time
import pickle
import gzip
import shutil

sock = socket.socket()
port = 6000
sock.bind(('',port))
sock.listen()
print("server started and listening")
client, address = sock.accept()
print(address)
next_frame_to_send=0;
data=''
num=0
#getting data from the client
x=0
data_get=client.recv(8192).decode()
while (True):
    data=data+data_get
    if(len(data_get)!=0):
        ack=int(data_get[0])
    next_frame_to_send=(next_frame_to_send+1)%2
    packet=str(next_frame_to_send)+str(ack)
    client.send(packet.encode())
    #getting data from the client
    data_get=client.recv(8192).decode()
    dat_get=str(data_get)
    #if end of the file break the loop
    if(data_get=="b''"):
        x=x+1
        break
fptr=open("destination.txt",'wb')
print("writing in the file")
c=fptr.write(data.encode())
#finding time for compression
start_time= time.time()
with open('destination.txt','rb') as f_input:
    with gzip.open('compressed_file.gz','wb') as f_output:
        shutil.copyfileobj(f_input,f_output)
end_time=time.time()
final_time= (end_time-start_time)/x
packet ="time_taken"+str(final_time)+" "+"seconds"
#sending packet to the server
client.sendall(packet.encode())


        
        

    
