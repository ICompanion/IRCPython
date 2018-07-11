# -*- coding: utf-8 -*-

from threading import Thread
import socket
from tkinter import *
import configparser
import webbrowser

def setConnection( username, serverP, portP, passwordP):
    global server
    global port
    global user
    global password
    global channel
    global joinedChannel
    global commands

    user = username
    server = serverP
    port = int(portP)
    password = passwordP
    channel = None
    joinedChannel = False
    commands = {"join", "leave", "part"}

def send_message(msg):
    message = msg + "\n"
    try:
        IRC.send(bytes(message, "ISO-8859-1"))
        if msg == "{quit}":
            IRC.close()
            windowChat.quit()
    except OSError as e:
        print(e)
        pass

def join_channel(channelEntry):
    global channel

    if channelEntry.get().startswith("#"):
        channel = channelEntry.get()
        msg ="JOIN " + channelEntry.get()
    else:
        channel = '#' + channelEntry.get()
        msg = "JOIN #" + channelEntry.get()
    try:
        send_message(msg)
    except Exception:
        pass

def leaveChannel(e):
    global channel
    if channel is not None:
        send_message("PART " + channel)
        channel = None

def listener():
    while True:
        try:
            msg = IRC.recv(1024).decode("ISO-8859-1")
            getMessage(msg)

            if msg.find("PING") != -1:
                pong = "PONG " + msg.split()[1] + "\r"
                send_message(pong)
                getMessage(pong)
        except OSError as e:
            print(e)
            break


def connect():
    global IRC
    IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        IRC.connect((socket.gethostbyname(server), int(port)))
        receive_thread = Thread(target=listener)
        receive_thread.start()
        send_command('NICK ' + user + '\r\n')
        send_command('USER ' + user + ' 0 * :' + user + '\r\n')
    except socket.error as e:

        print(e)

def close():
    global messageDisplay
    global IRC
    try:
        IRC.close()
        messageDisplay.configure(state=NORMAL)
        messageDisplay.delete(1.0, END)
        messageDisplay.insert(END, "Déconnecté de " + server)
        messageDisplay.configure(state=DISABLED)
    except socket.error as e:
        messageDisplay.configure(state=NORMAL)
        messageDisplay.insert(END, e)
        messageDisplay.configure(state=DISABLED)
        pass


def start():
    global server
    global port
    global user
    global password
    global channel
    global windowChat
    global messageDisplay
    global messageEntry

    windowChat = Tk()
    windowChat.geometry("800x600")
    windowChat.title("The Big Irski")
    label = Label(windowChat)

    menuBar = Menu(windowChat)
    windowChat['menu'] = menuBar

    serverMenu = Menu(menuBar)

    menuBar.add_cascade(label='Serveur', menu=serverMenu)
    menuBar.add_cascade(label='Aide')
    menuBar.add_cascade(label='A Propos')

    serverMenu.add_command(label='Connecter', command= lambda : serverConnection())
    serverMenu.add_command(label='Deconnecter', command= lambda : close())
    serverMenu.add_command(label='Favoris', command= lambda : getPrefered())

    messageDisplay = Text(windowChat, height=25, width=50)
    scroll = Scrollbar(messageDisplay)
    scroll.pack(side=RIGHT, fill=Y)
    messageDisplay.configure(state=DISABLED, yscrollcommand=scroll.set)
    scroll.config(command=messageDisplay.yview)

    messageEntry = Text(windowChat, height=5, width=75)
    scroll2 = Scrollbar(messageEntry)
    scroll2.pack(side=RIGHT, fill=Y)
    messageEntry.configure(yscrollcommand=scroll2.set)
    scroll2.config(command=messageEntry.yview)
    messageEntry.bind('<Return>', sendMessage)

    sendButton = Button(windowChat, text="Envoyer", command = lambda : sendMessage(""))

    chanLabel = Label(windowChat, text="Rejoindre un salon")
    chanEntry = Entry(windowChat)

    chanButton = Button(windowChat, text="Ok", command = lambda : join_channel(chanEntry))
    chanLeaving = Button(windowChat, text="Quitter le salon", command = lambda : leaveChannel(""))

    label.pack()
    messageDisplay.pack(padx=10, pady=10,fill=BOTH, expand=1)
    messageEntry.pack(padx=10, pady=10,fill=BOTH, expand=1)
    sendButton.pack(side="bottom", padx=10, pady=10)
    chanLabel.pack(anchor="w", padx=30, pady=5)
    chanEntry.pack(anchor="w", padx=28, pady=5)
    chanLeaving.pack(anchor="w", padx=42, pady=5)
    chanButton.pack(anchor="w", padx=70, pady=5)

    windowChat.mainloop()

def send_command(cmd):
    try:
        send_message(cmd)
    except Exception:
        pass

def sendMessage(e):
    msg = messageEntry.get("1.0", END)
    try:
        send_message("PRIVMSG " + channel + " " + msg)
    except Exception:
        pass
    getMessage(user + ": " + msg)
    messageEntry.delete(1.0, END)


def getMessage(msg):

    messages = msg.split(" ")
    try:
        for word in messages:
            if word.startswith("http"):
                messageDisplay.configure(state=NORMAL)
                messageDisplay.insert(END, word + " ", 'tag_url')
                messageDisplay.tag_config('tag_url', foreground='blue', underline=1)
                messageDisplay.tag_bind('tag_url', '<Button-1>', lambda e: webbrowser.open(word))
                messageDisplay.configure(state=DISABLED)
            else:
                messageDisplay.configure(state=NORMAL)
                messageDisplay.insert(END, word + " ")
                messageDisplay.configure(state=DISABLED)
    except:
        pass

def addPrefered(server, port, username, password):
    config = configparser.ConfigParser()
    print(config.has_section(server))
    if(config.has_section(server) == False):
        config[server] = {
                          'Port' : port,
                          'User' : username,
                          'Password': password
                         }
        with open('preferences.ini', 'a') as configFile:
            config.write(configFile)


def connectToIrc(window, server, port, user, password):
    setConnection(user, server, port, password)
    window.destroy()
    connect()
    send_message("REGISTER greg ririo2@hotmail.fr")



def listClicked(window, list):
    if(len(list.curselection()) > 0):
        config = configparser.ConfigParser()
        pref = list.get(list.curselection())

        config.read('preferences.ini')

        server = pref
        port = config[pref]['Port']
        user = config[pref]['User']
        password = config[pref]['Password']

        connectToIrc(window,server, port, user, password)


def deletePrefered(window, list):
    if(len(list.curselection()) > 0):
        config = configparser.ConfigParser()
        pref = list.get(list.curselection())
        config.read('preferences.ini')

        config.remove_section(pref)
        with open('preferences.ini', 'w') as f:
            config.write(f)

    window.destroy()
    getPrefered()

def getPrefered():
    preferedList = Tk()
    preferedList.geometry("300x300")

    list = Listbox(preferedList, activestyle='dotbox')
    list.pack(fill=BOTH, expand=1, padx=5, pady=5)

    config = configparser.ConfigParser()
    config.read('preferences.ini')
    preferences = config.sections()

    for pref in preferences:
        list.insert(END, pref)

    button = Button(preferedList, text="Connecter", command=lambda: listClicked(preferedList, list))
    button3 = Button(preferedList, text="Modifier", command=lambda: updatePrefered(preferedList, list))
    button2 = Button(preferedList, text="Supprimer des favoris", command=lambda: deletePrefered(preferedList, list))
    button.pack(side='left', padx=10, pady=10)
    button2.pack(side='right', pady=10, padx=10)
    button3.pack(side='bottom', pady=10, padx=10)


def changePrefered(server, port, user, password, window):

    config = configparser.ConfigParser()
    config.read('preferences.ini')
    config.set(server, 'port', port)
    config.set(server, 'user', user)
    config.set(server, 'password', password)

    with open('preferences.ini', 'w') as f:
        config.write(f)

    window.destroy()


def updatePrefered(preferedList, list):
    connectionWindow = Tk()
    connectionWindow.geometry("500x200")
    connectionWindow.resizable(False, False)
    connectionWindow.title("Server Connection")

    server = ""
    port = ""
    user = ""
    password = ""

    if len(list.curselection()) > 0:
        config = configparser.ConfigParser()
        pref = list.get(list.curselection())
        server = pref
        config.read('preferences.ini')
        port = config[pref]['Port']
        user = config[pref]['User']
        password = config[pref]['Password']

    serverLabel = Label(connectionWindow, text="Host").grid(row=0)
    portLabel = Label(connectionWindow, text="Port").grid(row=0, column=5, pady=20)
    userLabel = Label(connectionWindow, text="User").grid(row=3)
    passwordLabel = Label(connectionWindow, text="Password")


    serverStr = Entry(connectionWindow)
    portStr = Entry(connectionWindow)
    userStr = Entry(connectionWindow)
    passwordStr = Entry(connectionWindow, show="*")

    validateButton = Button(connectionWindow, text="Enregistrer", command=lambda : changePrefered(serverStr.get(), portStr.get(), userStr.get(), passwordStr.get(), connectionWindow))
    cancelButton = Button(connectionWindow, text="Annuler", command= connectionWindow.destroy)

    serverStr.grid(row=0, column=1, padx=30)
    portStr.grid(row=0, column=6)
    userStr.grid(row=3, column=1)
    passwordStr.grid(row=3, column=6)

    validateButton.grid(row=8, column=2)
    cancelButton.grid(row=8, column=1, pady=40)

    serverStr.insert(0, server)
    portStr.insert(0, port)
    userStr.insert(0, user)
    passwordStr.insert(0, password)

    preferedList.destroy()


def serverConnection():
    connectionWindow = Tk()
    connectionWindow.geometry("500x200")
    connectionWindow.resizable(False, False)
    connectionWindow.title("Server Connection")

    serverLabel = Label(connectionWindow, text="Host").grid(row=0)
    portLabel = Label(connectionWindow, text="Port").grid(row=0, column=5, pady=20)
    userLabel = Label(connectionWindow, text="User").grid(row=3)
    passwordLabel = Label(connectionWindow, text="Password").grid(row=3, column=5)

    serverStr = Entry(connectionWindow)
    portStr = Entry(connectionWindow)
    userstr = Entry(connectionWindow)
    passwordStr = Entry(connectionWindow, show="*")

    validateButton = Button(connectionWindow, text="Connection", command=lambda : connectToIrc(connectionWindow, serverStr.get(), portStr.get(), userstr.get(), passwordStr.get()))
    cancelButton = Button(connectionWindow, text="Annuler", command= connectionWindow.destroy)
    preferedButton = Button(connectionWindow, text="Ajouter aux favoris", command= lambda : addPrefered(serverStr.get(), portStr.get(), userstr.get(), passwordStr.get()))

    serverStr.grid(row=0, column=1, padx=30)
    portStr.grid(row=0, column=6)
    userstr.grid(row=3, column=1)
    passwordStr.grid(row=3, column=6)

    validateButton.grid(row=8, column=2)
    cancelButton.grid(row=8, column=1, pady=40)
    preferedButton.grid(row=8, column=6)


start()