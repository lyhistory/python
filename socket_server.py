# -*- coding: UTF-8 -*-
import sys
import socket
import os

class Server:
    def __init__(self, ip, port):
        self.ip=ip
        self.port=port
        self.buffersize=10240

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.ip,self.port))
            s.listen(10)
            print("waiting...")
            while True:
                try:
                    conn,addr=s.accept()
                    print("connected:",addr[0],",",addr[1])
                    while True:
                        data=conn.recv(self.buffersize)
                        if not data:
                            print("nothing")
                            break
                        else:
                            print("recevied:",data)
                            self.executecmd(conn,data)
                    conn.close()
                except socket.error as e:
                    print(e)
                    conn.close()
        except socket.error as e:
            print(e)
            sys.exit()
        finally:
            s.close()

    def executecmd(self,conn,data):
        try:
            message = data.decode("utf-8")
            if os.path.isfile(message):
                filesize = str(os.path.getsize(message))
                print("file size:",filesize)
                conn.send(filesize)
                data = conn.recv(self.buffersize)
                print("start to send")
                f = open(message,'rb')
                for line in f:
                    conn.send(line)
            else:
                conn.send(('0001'+os.popen(message).read()).encode("utf-8"))
        except:
            raise
if __name__ == '__main__':
    server = Server("",8080)
    server.start()
