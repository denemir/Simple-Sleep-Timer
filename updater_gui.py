import tkinter
from tkinter import ttk

from gui_common import GuiCommon

class UpdaterGui:
    def __init__(self, config=None, parent=None, latest_version=None):
        self.parent = parent
        self.window = tkinter.Toplevel(parent)
        self.window.transient(parent)
        self.window.focus_force()
        self.window.grab_set()
        icon_path = GuiCommon.resource_path('icon.ico')
        self.window.iconbitmap(icon_path)
        self.config = config

        # setup window
        self.window.title('Updater')
        self.window.minsize(300, 100)
        self.window.resizable(False, False)
        GuiCommon.center_window(self.parent)
        GuiCommon.center_window(self.window)

        # vars
        self.current_version = self.config.version
        self.latest_version = latest_version

    def initialize_window(self):
        # vars
        top_frame = ttk.Frame(self.window)
        top_frame.pack(padx=3, pady=3, side="top", fill="x")

        notice = ttk.Label(top_frame,
                            text=f"A new update is available! Version {self.latest_version}")
        notice.pack()

        current_ver_notice = ttk.Label(top_frame, text=f"Current Version: {self.current_version}")
        current_ver_notice.pack()

        self.render_buttons(top_frame)

    def render_buttons(self, frame=None):
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=1, pady=(0, 10))
        ttk.Button(btn_frame, text="Skip", command=self.on_skip).pack(side="left", padx=(1, 5))
        ttk.Button(btn_frame, text="Remind me next time", command=self.on_remind).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Download", command=self.on_download).pack(side="left", padx=(0, 1))

    def on_skip(self):
        self.config.set_skip_version(version=self.latest_version)
        self.window.destroy()

    def on_remind(self):
        self.window.destroy()

    def on_download(self):
        self.config.update_application()