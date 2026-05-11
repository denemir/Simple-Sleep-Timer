import tkinter
from tkinter import ttk

from gui_common import GuiCommon

class UpdaterGui:
    def __init__(self, config=None, parent=None, latest_version=None):
        self.window = tkinter.Toplevel()
        self.window.focus_force()
        self.config = None

        # setup window
        self.window.title('Updater')
        self.window.minsize(300, 100)
        self.window.resizable(False, False)
        # self.window.transient(parent)
        self.window.grab_set()

        # vars
        self.current_version = None
        self.latest_version = None

    @staticmethod
    def initialize_window(config=None, latest_version=None):
        # vars
        current_version = config.version

        root = tkinter.Tk()
        root.title("Updater")
        top_frame = ttk.Frame(root)
        top_frame.pack(padx=3, pady=3, side="top", fill="x")
        GuiCommon.center_window(root)

        notice = ttk.Label(top_frame,
                            text=f"A new update is available! Version {latest_version}")
        notice.pack()

        current_ver_notice = ttk.Label(top_frame, text=f"Current Version: {current_version}")
        current_ver_notice.pack()

        UpdaterGui.render_buttons(top_frame)

    @staticmethod
    def render_buttons(frame=None):
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 10))
        ttk.Button(btn_frame, text="Skip", command=UpdaterGui.on_skip).pack(side="left")
        ttk.Button(btn_frame, text="Remind me next time", command=UpdaterGui.on_remind).pack(side="left")
        ttk.Button(btn_frame, text="Download", command=UpdaterGui.on_download).pack(side="right")

    @staticmethod
    def on_skip():
        print("skip")

    @staticmethod
    def on_remind():
        print("remind")

    @staticmethod
    def on_download():
        print("download")