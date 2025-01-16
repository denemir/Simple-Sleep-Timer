import os
import platform
import subprocess
import ctypes

from gui import GUI
from config import Config
from timer import Timer


class App:
    def __init__(self):
        self.duration = 0

        # options
        self.default_options = ["15 min", "30 min", "1 hrs", "90 min", "2 hrs", "3 hrs"]
        self.default_option = None  # default options only
        self.custom_options = None  # custom options only
        self.all_options = None  # all options collectively

        self.timer = Timer(callback=self.sleep, update_call=self.update_timer_dropdown)
        self.config = Config()
        self.parse_file_for_default_option()
        self.version = self.config.version
        self.gui = GUI(prog=self, theme=self.config.get_theme(), default_option=self.default_option, version=self.version)

    def start_timer(self, selection=None):
        self.timer.start_timer(selection=selection, on_complete=self.sleep)

    def pause_timer(self):
        self.timer.pause_timer()

    def cancel_timer(self):
        self.timer.cancel_timer()
        self.duration = 0

    def save_timer(self, duration, unit):
        self.config.add_timer(duration=duration, unit=unit)

    def clear_timers(self):
        self.config.delete_timers()

    def sleep(self):
        print('Merry Christmas!')

        # determine OS
        system = platform.system()
        try:
            if system == "Windows":
                # ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2) monitor off
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif system == "Darwin":
                subprocess.run(["pmset", "sleepnow"])
            elif system == "Linux":
                subprocess.run(["systemctl", "suspend"])
        except Exception as e:
            print(f"An error occurred while putting the system to sleep: {e}")

        # reset buttons
        self.gui.toggle_start_stop_buttons()

    def parse_file_for_default_option(self):
        self.default_option = self.config.get_default_option()

    def get_default_option(self):
        return self.default_option

    def get_all_options(self):
        self.custom_options = self.config.get_timers()

        self.all_options = self.default_options + [opt for opt in self.custom_options if
                                                   opt not in self.default_options]

        if self.default_option in self.all_options:
            index = self.all_options.index(self.default_option)
            self.all_options[index] = self.all_options[index] + " ★"

        return self.all_options

    def get_remaining_time(self):
        return self.timer.get_remaining_time()

    def set_default_option(self, duration=None, unit=None):
        # check if option with star exists in list of options
        if (self.default_option is not None and self.default_option + " ★") in self.all_options:
            index = self.all_options.index(self.default_option + " ★")

            # update all options to ensure star is no longer on old default option
            self.all_options[index] = self.all_options[index].replace(f" ★", "")
        self.default_option = str(duration) + ' ' + unit

    def set_default_timer(self, duration, unit):
        self.config.set_default_option(duration=duration, unit=unit)
        self.set_default_option(duration=duration, unit=unit)
        self.gui.refresh_timers()

    def update_timer_dropdown(self):
        self.gui.update_timer_display()

    def update_theme(self, theme=None):
        self.config.set_theme(theme=theme)

    def run(self):
        self.gui.initialize_gui()


if __name__ == "__main__":
    prog = App()
    prog.run()
