#!/usr/bin/env python
#coding:utf-8
import socket
import threading
import time
import logging
import sys

logging.basicConfig(level=logging.DEBUG)

class Danmu:

    def __init__(self, ip, port):
        self.threading_count = 0
        self.listen_ip = ip
        self.listen_port = port
        self.sock = None

    def start_server(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 60)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 4)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 15)



        sock.bind((self.listen_ip, self.listen_port))
        sock.listen(5)
        self.sock = sock

        while True:
            logging.info("create socket. waiting client...  %d" % self.threading_count)
            conn, addr = self.sock.accept()
            # 收到请求丢给线程去处理, 线程不退出，保持一直链接
            t = threading.Thread(target=self.response, args=(conn, addr))
            t.start()
            # self.response(conn, addr)

    def response(self, conn, addr):
        self.threading_count +=1
        logging.info("server response %s:%s" % (str(addr[0]), str(addr[1])))
        creattime = time.time()
        while True:
            # 客户端超过20秒没有发送任何数据，则关闭链接
            if time.time() - creattime > 20:
                break;

            try:
                data = conn.recv(2048).strip()
                if data:
                    creattime = time.time()
                    print data
                    # do some things
            except Exception, e:
                logging.error(e.error())
                break

        # 循环退出，退出线程
        self.threading_count -=1
        logging.info("timeout exit!")
        conn.sendall("timeout")
        conn.close()



if __name__ == '__main__':
    d = Danmu('0.0.0.0', 10101)
    d.start_server()
