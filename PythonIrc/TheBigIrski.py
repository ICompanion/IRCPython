from Irc import Irc
import win32gui, win32con

#The_program_to_hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(The_program_to_hide , win32con.SW_HIDE)


try:
    open("preferences.ini", "r")
except:
    open("preferences.ini","w+")

Irc.start()
