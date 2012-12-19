import asyncore
import socket
import shlex

class EchoHandler(asyncore.dispatcher_with_send):

    def __init__(self, ident, *args, **kwargs):
        
        asyncore.dispatcher_with_send.__init__(self, *args, **kwargs)

        self.ident = ident
        self.send("your id is %s\n" % str(ident))
        

    def handle_read(self):
        data = self.recv(8192)
        if data:
            command = shlex.split(data)
            if command[0] not in ["help", "buzzer", "say"]:
                self.send("command %s not found\n" % command[0])
            else:
                self.send(data)

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            
            greeting = r""" 
Welcome to the Quizshow!
========================================  

___________________________________ 
< Send "help" for more information! >
 ----------------------------------- 
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

"""
            sock.send(greeting)
            handler = EchoHandler(addr, sock)


server = EchoServer('localhost', 8080)
asyncore.loop()
