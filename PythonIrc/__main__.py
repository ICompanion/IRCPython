from tkinter import *
import configparser


def main():
    tkWindow = Tk()

    tkWindow.title("Le petit de Chat de Thibauuuuud")
    label = Label(tkWindow)

    menuBar = Menu(tkWindow)
    tkWindow['menu'] = menuBar

    serverMenu = Menu(menuBar)

    menuBar.add_cascade(label='Serveur', menu=serverMenu)
    menuBar.add_cascade(label='Aide')
    menuBar.add_cascade(label='A Propos')

    serverMenu.add_command(label='Connecter', command= lambda : serverConnection())
    serverMenu.add_command(label='Favoris', command= lambda : getPrefered())


    textZone = Text(tkWindow, height=25, width=50)
    textZone.configure(state=DISABLED)

    entryText = Text(tkWindow, height=5, width=75)

    sendButton = Button(tkWindow, text="Envoyer", command = lambda : sendText(textZone, entryText))

    label.pack()
    textZone.pack(padx=10, pady=10,fill=BOTH, expand=1)
    entryText.pack(padx=10, pady=10,fill=BOTH, expand=1)
    sendButton.pack(side="bottom", padx=10, pady=10)

    tkWindow.mainloop()


def sendText(text1, text2):
    text1.configure(state=NORMAL)
    text1.insert(END, text2.get("1.0", END))
    text1.configure(state=DISABLED)
    text2.delete(1.0, END)


def addPrefered(server, port, username):
    config = configparser.ConfigParser()
    config[server] = {
                      'Port' : port,
                      'User' : username
                     }
    with open('preferences.ini', 'w') as configFile:
        config.write(configFile)


def connectToIrc(pref):
    print("connected to " + str(pref))


def getPrefered():
    preferedList = Tk()
    preferedList.geometry("200x200")

    list = Listbox(preferedList)
    list.pack(fill=BOTH, expand=1)

    config = configparser.ConfigParser()
    config.read('preferences.ini')
    preferences = config.sections()

    for pref in preferences:
        list.insert(END, pref)

    list.bind("<<ListBoxSelect>>", connectToIrc(list.get(list.curselection())))



def serverConnection():
    connectionWindow = Tk()
    connectionWindow.geometry("500x200")
    connectionWindow.title("Server Connection")

    serverLabel = Label(connectionWindow, text="Host").grid(row=0)
    portLabel = Label(connectionWindow, text="Port").grid(row=0, column=5, pady=20)
    userLabel = Label(connectionWindow, text="User").grid(row=3)
    passwordLabel = Label(connectionWindow, text="Password").grid(row=3, column=5)

    serverStr = Entry(connectionWindow)
    portStr = Entry(connectionWindow)
    userstr = Entry(connectionWindow)
    passwordStr = Entry(connectionWindow, show="*")

    validateButton = Button(connectionWindow, text="Connexion")
    cancelButton = Button(connectionWindow, text="Cancel", command= connectionWindow.destroy)
    preferedButton = Button(connectionWindow, text="Ajouter aux favoris", command= lambda : addPrefered(serverStr.get(), portStr.get(), userstr.get()))

    serverStr.grid(row=0, column=1, padx=30)
    portStr.grid(row=0, column=6)
    userstr.grid(row=3, column=1)
    passwordStr.grid(row=3, column=6)

    validateButton.grid(row=8, column=2)
    cancelButton.grid(row=8, column=1, pady=40)
    preferedButton.grid(row=8, column=6)

main()