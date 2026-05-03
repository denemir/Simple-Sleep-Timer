import tkinter
from tkinter import ttk

from gui_common import GuiCommon

class PreferencesGui:
    def __init__(self, parent, callback):
        self.window = tkinter.Toplevel(parent)
        self.callback = callback

        # setup window
        self.window.title('Preferences')
        self.window.minsize(200, 50)
        self.window.resizable(True, True)
        self.window.transient(parent)  # window modal
        self.window.grab_set()

    def initialize_gui(self):
        top_frame = ttk.Frame(self.window)
        top_frame.pack(padx=3, pady=3, side="top", fill="x")
        GuiCommon.center_window(self.window)