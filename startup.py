import os.path
import sys
import winreg

APP_NAME = "SimpleSleepTimer"

class Startup:
    @staticmethod
    def get_executable_path(background: bool = False) -> str:
        if getattr(sys, 'frozen', False):
            return sys.executable
        else:
            path = f'pythonw.exe "{os.path.abspath(sys.argv[0])}"'

        if background:
            path += " --background"
        return path

    @staticmethod
    def set_startup(enabled: bool, background: bool = False):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, Startup.get_executable_path(background))
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass # already removed

    @staticmethod
    def is_startup_enabled() -> bool:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.QueryValueEx(key, APP_NAME)
                return True
        except FileNotFoundError:
            return False