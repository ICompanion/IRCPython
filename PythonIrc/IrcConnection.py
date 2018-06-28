import string, time
from threading import Thread
import socket

class IrcConnection:

    server = ""
    port = 0000
    user = ""
    channel=""



    def __init__(self, username, channel, server, port):
        self.user = username
        self.server = server
        self.port = int(port)
        self.channel = channel

    def connect(self):
        global IRC
        IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IRC.connect((self.server, self.port))

    def sendCommand(self, cmd, message):
        command = "{} {}\r\n".format(cmd, message)
        IRC.send(command)

    def send_message(self, msg):
        command = "PRIVMSG {}".format(self.channel)
        message = ":" + msg
        self.send_cmd(command, msg)

    def join_channel(self):
        cmd = "JOIN"
        channel = self.channel
        self.send_cmd(cmd, channel)

    def listener(self):
        while(1):
            buffer = IRC.recv(1024)
            msg = string.split(buffer)

            yield msg[0]

