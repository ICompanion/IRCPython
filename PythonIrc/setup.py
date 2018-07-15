"""Installation file"""

from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

bdist_msi_options = {
    "upgrade_code": "{96a85bac-52af-4019-9e94-3afcc9e1ad0c}"
    }

setup(
    name = "TheBigIrski",
    version = "1.0",
    description = "Client Irc",
    options={"build_exe": {"packages": ["Irc","win32gui", "win32con", "threading",
                                        "socket", "tkinter", "configparser", "webbrowser"],
                           "include_files": ["TheBIgIrski.py",
                                             os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                                             os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')],
                            'include_msvcr': True,
                           },
             "bdist_msi": bdist_msi_options
             },
    executables = [Executable("TheBigIrski.py", base="Win32GUI", shortcutName="TheBigIrski",
                                shortcutDir='DesktopFolder')],
)
