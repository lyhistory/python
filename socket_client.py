import sys
import socket
import os
import re

class Client:
    def __init__(self, ip, port):
        self.ip=ip
        self.port=port
        self.buffersize=10240
    def connect(self):
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print(e)
            sys.exit()
        try:
            s.connect((self.ip, self.port))
            while True:
                message = input('> ')
		#raw_input('> ')
		#print("input=",message)
                if not message:
                    break
                s.send(bytes(message,'utf-8'))
                data = s.recv(self.buffersize)
                if not data:
                    print("nothing")
                    break
                if re.search("^0001",data.decode('utf-8','ignore')):
                    print(data.decode('utf-8')[4:])
                else:
                    s.send(("file size recived").encode())
                    file_total_size = int(data.decode())
                    received_size=0
                    f=open(os.path.split(message)[-1],"wb")
                    while received_size < file_total_size:
                        data=s.recv(self.buffersize)
                        f.write(data)
                        received_size+=len(data)
                        print("received:",received_size)
                    f.close()
                    print("done total:",file_total_size," recived size:",received_size)
        except socket.error as e:
            print(e)
            sys.exit()

if __name__ == '__main__':
    client = Client("192.168.207.4",8080)
    client.connect()
    sys.exit()
