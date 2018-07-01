import string
from threading import Thread
import socket
from tkinter import *
import configparser

def setConnection( username, channelP, serverP, portP):
    global server
    global port
    global user
    global channel

    user = username
    server = serverP
    port = int(portP)
    channel = channelP

def send_message(msg):
    message = user + ":" + msg
    IRC.send(bytes(message, "utf8"))
    if msg == "{quit}":
        IRC.close()
        windowChat.quit()

def join_channel():
    cmd = "JOIN"

def listener():
    while True:
        try:
            msg = IRC.recv(BUFSIZ).decode("utf8")
            getMessage(msg)
        except OSError:
            break


def connect():
    global IRC
    IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        IRC.connect((socket.gethostbyname(server), int(port)))
        receive_thread = Thread(target=listener)
        receive_thread.start()
    except socket.error as e:

        print(e)

def start():
    global server
    global port
    global user
    global channel
    global windowChat
    global messageDisplay
    global messageEntry
    global BUFSIZ

    BUFSIZ = 1024
    windowChat = Tk()

    windowChat.title("The Big Irski")
    label = Label(windowChat)

    menuBar = Menu(windowChat)
    windowChat['menu'] = menuBar

    serverMenu = Menu(menuBar)

    menuBar.add_cascade(label='Serveur', menu=serverMenu)
    menuBar.add_cascade(label='Aide')
    menuBar.add_cascade(label='A Propos')

    serverMenu.add_command(label='Connecter', command= lambda : serverConnection())
    serverMenu.add_command(label='Favoris', command= lambda : getPrefered())

    messageDisplay = Text(windowChat, height=25, width=50)
    messageDisplay.configure(state=DISABLED)

    messageEntry = Text(windowChat, height=5, width=75)

    sendButton = Button(windowChat, text="Envoyer", command = lambda : sendText())

    label.pack()
    messageDisplay.pack(padx=10, pady=10,fill=BOTH, expand=1)
    messageEntry.pack(padx=10, pady=10,fill=BOTH, expand=1)
    sendButton.pack(side="bottom", padx=10, pady=10)
    windowChat.mainloop()


def sendText():
    msg = messageEntry.get("1.0", END)
    send_message(msg)
    getMessage(msg)

def getMessage(msg):
    messageDisplay.insert(END, msg)

def addPrefered(server, port, username):
    config = configparser.ConfigParser()
    config[server] = {
                      'Port' : port,
                      'User' : username
                     }
    with open('preferences.ini', 'a') as configFile:
        config.write(configFile)


def connectToIrc(window, server, port, user):
    setConnection(user, '#EpiKnet', server, port)
    window.destroy()
    connect()


def listClicked(window, list):
    if(len(list.curselection()) > 0):
        config = configparser.ConfigParser()
        pref = list.get(list.curselection())

        config.read('preferences.ini')

        server = pref
        port = config[pref]['Port']
        user = config[pref]['User']

        connectToIrc(window,server, port, user)


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
    button2 = Button(preferedList, text="Supprimer des favoris", command=lambda: deletePrefered(preferedList, list))
    button.pack(side='left', padx=10, pady=10)
    button2.pack(side='right', pady=10, padx=10)


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

    validateButton = Button(connectionWindow, text="Connexion", command=lambda : connectToIrc(connectionWindow, serverStr.get(), portStr.get(), userstr.get()))
    cancelButton = Button(connectionWindow, text="Cancel", command= connectionWindow.destroy)
    preferedButton = Button(connectionWindow, text="Ajouter aux favoris", command= lambda : addPrefered(serverStr.get(), portStr.get(), userstr.get()))

    serverStr.grid(row=0, column=1, padx=30)
    portStr.grid(row=0, column=6)
    userstr.grid(row=3, column=1)
    passwordStr.grid(row=3, column=6)

    validateButton.grid(row=8, column=2)
    cancelButton.grid(row=8, column=1, pady=40)
    preferedButton.grid(row=8, column=6)


start()