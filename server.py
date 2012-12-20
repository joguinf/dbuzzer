import asyncore
import socket
import shlex

class EchoHandler(asyncore.dispatcher_with_send):

    def __init__(self, ident, *args, **kwargs):

        # call superclass init
        asyncore.dispatcher_with_send.__init__(self, *args, **kwargs)

        # set ident and name
        self.ident = ident
        self.nick  = str(ident)

    def handle_read(self):
    
        data = self.recv(8192)

        methods = {"help": self.print_help,
                   "nick": self.set_nick,
                   "list": self.list_players,
                   "say" : self.say}

        if data:
        
            message = shlex.split(data)
        
            if message[0] not in methods:
                self.send("command %s not found\n\n" % message[0])
            else:
                methods[message[0]](message)
              
    def print_help(self, *args, **kwds):

        message = r"""
USAGE:

    help ...................... print out help page
    list ...................... list players
    nick ...................... show your own nick 
    nick Larry ................ set your nick to "Larry"
    buzzer .................... press the buzzer button
    say Hello ................. say "Hello" to the people
    
"""
        self.send(message)

    def set_nick(self, *args, **kwds):
    
        if len(args[0]) == 1:
        
            if str(self.ident) == self.nick:
                self.send('first set your nickname with "nick nickname"\n\n')
            else:
                self.send("your nick is: %s\n\n" % self.nick)
        else:
            self.nick="%s(%s)" % (" ".join(args[0][1:]), self.ident[1])
            self.send('your nick was changed to: %s\n\n' % self.nick)

    def list_players(self, *args, **kwds):

        self.send(", ".join(server.get_clients())+"\n\n")

    def say(self, *args, **kwds):

        if len(args[0]) > 1:
        
            if str(self.ident) == self.nick:
                self.send('first set your nickname with "nick nickname"\n\n')
            else:
                message = " ".join(args[0][1:])
                server.broadcast("%s: %s\n" % (self.nick, message))
        else:
            self.send("(said nothing)\n\n")

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        
        self.connections = []

    def broadcast(self, text, newline=True):

        for client in self.connections:
            try:
                client.send(text+"\n" if newline else "")
            except:
                pass

    def get_clients(self):
    
        clients = []
        
        for client in self.connections:
            try:
                if client.nick == str(client.ident):
                    clients.append("no_nick_set!(%s)" % client.ident[1])
                else:
                    clients.append(client.nick)
            except:
                pass
        
        return clients

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

 _____________________________________ 
/ Set your nick with "nick Larry" and \
\ list the help page with "help"      /
 ------------------------------------- 
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

"""
            sock.send(greeting)
            handler = EchoHandler(addr, sock)
            self.connections.append(handler)

server = EchoServer('localhost', 8080)
asyncore.loop()
