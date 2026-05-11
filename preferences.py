import logging
import tkinter
from gc import enable
from tkinter import ttk

from gui_common import GuiCommon
from startup import Startup


class PreferencesGui:
    def __init__(self, parent=None, callback=None, config=None):
        self.window = tkinter.Toplevel(parent)
        self.window.focus_force()
        self.callback = callback
        self.config = config

        # setup window
        self.window.title('Preferences')
        self.window.minsize(300, 100)
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        # tab values
        self.run_on_startup = tkinter.BooleanVar(value=self.config.get_preference("run_on_startup"))
        self.startup_in_background = tkinter.BooleanVar(value=self.config.get_startup_in_background())
        self.minimize_on_close = tkinter.BooleanVar(value=self.config.get_minimize_on_close())
        self.enable_notifications = tkinter.BooleanVar(value=self.config.get_enable_notifications())
        self.enable_online_updater = tkinter.BooleanVar(value=self.config.get_enable_online_updater())

        # toggleable items
        self.startup_in_background_box = None

    def initialize_gui(self):
        top_frame = ttk.Frame(self.window)
        top_frame.pack(side="top", fill="x")
        GuiCommon.center_window(self.window)

        # tabs
        tab_style = ttk.Style()
        tab_style.configure("TNotebook.Tab", focuscolor=tab_style.configure(".")["background"])
        tab_style.configure("TNotebook", borderwidth=0, tabmargins=0, padding=0)

        tab_control = ttk.Notebook(top_frame)
        interface_tab = ttk.Frame(tab_control)
        notification_tab = ttk.Frame(tab_control)
        other_tab = ttk.Frame(tab_control)

        tab_control.add(interface_tab, text="Interface")
        tab_control.add(notification_tab, text="Notifications")
        tab_control.add(other_tab, text="Other")

        tab_control.pack(expand=1, fill="both")
        tab_control.pack_propagate(False)

        self.render_interface_tab(interface_tab)
        self.render_notification_tab(notification_tab)
        self.render_other_tab(other_tab)

    def render_interface_tab(self, tab):
        run_on_startup_box = ttk.Checkbutton(tab,
             text="Run on startup", variable=self.run_on_startup,
             command=self.on_toggle_run_on_startup
        )
        self.startup_in_background_box = ttk.Checkbutton(tab,
            text="Startup in background", variable=self.startup_in_background,
            command=lambda: [self.config.set_startup_in_background(
            self.startup_in_background.get()
            ),
            self.set_startup()],
            state=(
                tkinter.NORMAL if self.run_on_startup.get() else tkinter.DISABLED)
        )
        minimize_on_close_box = ttk.Checkbutton(tab,
            text="Minimize on close", variable=self.minimize_on_close,
            command=lambda: self.config.set_minimize_on_close(
                self.minimize_on_close.get()
        ))

        checkboxes = [
            run_on_startup_box,
            self.startup_in_background_box,
            minimize_on_close_box
        ]

        self.pack_checkboxes(checkboxes=checkboxes)

    def render_notification_tab(self, tab):
        enable_notifications_box = ttk.Checkbutton(tab,
           text="Enable Notifications",
           variable=self.enable_notifications,
           command=lambda: self.config.set_enable_notifications(
               self.enable_notifications.get()
           ))

        checkboxes = [
            enable_notifications_box
        ]

        self.pack_checkboxes(checkboxes=checkboxes)

    def render_other_tab(self, tab):
        enable_online_updater_box = ttk.Checkbutton(tab,
            text="Enable Online Updater",
            variable=self.enable_online_updater,
            command=None
        )

        checkboxes = [
            enable_online_updater_box
        ]

        self.pack_checkboxes(checkboxes=checkboxes)

    def on_toggle_run_on_startup(self):
        self.config.set_run_on_startup(self.run_on_startup.get())

        if not self.run_on_startup.get():
            self.config.set_startup_in_background(False)
            self.startup_in_background.set(False)

        self.toggle_startup_in_background_box()

        self.set_startup()

    def toggle_startup_in_background_box(self):
        self.startup_in_background_box.config(state=(tkinter.NORMAL if self.run_on_startup.get() else tkinter.DISABLED))

    def set_startup(self):
        Startup.set_startup(enabled=self.run_on_startup.get(),
                            background=self.startup_in_background.get())

    @staticmethod
    def pack_checkboxes(checkboxes=None):
        for box in checkboxes:
            box.pack(anchor="w", padx=10, pady=2)