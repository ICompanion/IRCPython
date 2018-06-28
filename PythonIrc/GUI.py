from tkinter import *
import configparser
from IrcConnection import IrcConnection

class GUI:

    tkWindow = None

    def __init__(self):
        tkWindow = Tk()

        tkWindow.title("The Big Irski")
        label = Label(tkWindow)

        menuBar = Menu(tkWindow)
        tkWindow['menu'] = menuBar

        serverMenu = Menu(menuBar)

        menuBar.add_cascade(label='Serveur', menu=serverMenu)
        menuBar.add_cascade(label='Aide')
        menuBar.add_cascade(label='A Propos')

        serverMenu.add_command(label='Connecter', command= lambda : self.serverConnection())
        serverMenu.add_command(label='Favoris', command= lambda : self.getPrefered())


        textZone = Text(tkWindow, height=25, width=50)
        textZone.configure(state=DISABLED)

        entryText = Text(tkWindow, height=5, width=75)

        sendButton = Button(tkWindow, text="Envoyer", command = lambda : self.sendText(textZone, entryText))

        label.pack()
        textZone.pack(padx=10, pady=10,fill=BOTH, expand=1)
        entryText.pack(padx=10, pady=10,fill=BOTH, expand=1)
        sendButton.pack(side="bottom", padx=10, pady=10)

        tkWindow.mainloop()


    def sendText(self, text1, text2):
        text1.configure(state=NORMAL)
        text1.insert(END, text2.get("1.0", END))
        text1.configure(state=DISABLED)
        IrcConnection.send_message(text2.get("1.0", END))
        text2.delete(1.0, END)

    def getMessage(self):
        return;

    def addPrefered(self, server, port, username):
        config = configparser.ConfigParser()
        config[server] = {
                          'Port' : port,
                          'User' : username
                         }
        with open('preferences.ini', 'a') as configFile:
            config.write(configFile)


    def connectToIrc(self, window,server, port, user):
        irc = IrcConnection(user, '#EpiKnet', server, port)
        irc.connect()


    def listClicked(self, window, list):
        if(len(list.curselection()) > 0):
            config = configparser.ConfigParser()
            pref = list.get(list.curselection())

            window.destroy()

            config.read('preferences.ini')

            server = pref
            port = config[pref]['Port']
            user = config[pref]['User']

            self.connectToIrc(server, port, user)


    def deletePrefered(self, window, list):
        if(len(list.curselection()) > 0):
            config = configparser.ConfigParser()
            pref = list.get(list.curselection())
            config.read('preferences.ini')

            config.remove_section(pref)
            with open('preferences.ini', 'w') as f:
                config.write(f)

        window.destroy()
        self.getPrefered()

    def getPrefered(self):
        preferedList = Tk()
        preferedList.geometry("300x300")

        list = Listbox(preferedList, activestyle='dotbox')
        list.pack(fill=BOTH, expand=1, padx=5, pady=5)

        config = configparser.ConfigParser()
        config.read('preferences.ini')
        preferences = config.sections()

        for pref in preferences:
            list.insert(END, pref)

        button = Button(preferedList, text="Connecter", command=lambda: self.listClicked(preferedList, list))
        button2 = Button(preferedList, text="Supprimer des favoris", command=lambda: self.deletePrefered(preferedList, list))
        button.pack(side='left', padx=10, pady=10)
        button2.pack(side='right', pady=10, padx=10)


    def serverConnection(self):
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

        validateButton = Button(connectionWindow, text="Connexion", command=lambda : self.connectToIrc(connectionWindow, serverStr.get("1.0", END), portStr.get("1.0", END), userstr.get("1.0", END)))
        cancelButton = Button(connectionWindow, text="Cancel", command= connectionWindow.destroy)
        preferedButton = Button(connectionWindow, text="Ajouter aux favoris", command= lambda : self.addPrefered(serverStr.get(), portStr.get(), userstr.get()))

        serverStr.grid(row=0, column=1, padx=30)
        portStr.grid(row=0, column=6)
        userstr.grid(row=3, column=1)
        passwordStr.grid(row=3, column=6)

        validateButton.grid(row=8, column=2)
        cancelButton.grid(row=8, column=1, pady=40)
        preferedButton.grid(row=8, column=6)
