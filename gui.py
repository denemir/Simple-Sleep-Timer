import tkinter
import tkinter.messagebox
import webbrowser
from tkinter import ttk
from PIL import Image, ImageTk
import sv_ttk


class GUI:
    def __init__(self, prog=None, default_option=None, theme=None, version=None):
        self.root = tkinter.Tk()
        self.prog = prog
        self.options = self.prog.get_all_options()
        self.default_option = default_option
        self.theme = theme
        self.version = version

        # main window
        self.timer_dropdown = None
        self.selected_timer = None
        self.start_button = None
        self.stop_button = None
        self.pause_button = None
        self.add_timer_button = None
        self.top_frame = None
        self.menu_bar = None

        # timer display
        self.timer_display = None
        self.running = False
        self.paused = False

        # add timer modal
        self.input_box = None
        self.unit_dropdown = None
        self.save_button = None

    def initialize_gui(self):
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(padx=5, pady=5, side="top", fill="x")

        # setup window
        self.root.title('Sleep Timer')
        self.root.minsize(250, 75)
        self.root.resizable(False, False)
        self.center_window(self.root)
        self.set_theme()


        # add menu options & buttons
        self.menu_bar = tkinter.Menu(self.root)

        # file menu
        file_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        file_menu.add_cascade(label="Preferences", command=self.feature_not_implemented_warning)
        file_menu.add_cascade(label="Toggle Theme", command=self.toggle_theme)
        file_menu.add_cascade(label="Version: " + self.version, state="disabled")
        file_menu.add_separator()
        file_menu.add_cascade(label="Check me out!", command=self.github)
        self.menu_bar.add_cascade(label="File", menu=file_menu)


        # help menu
        help_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        help_menu.add_cascade(label="Report a Bug", command=self.report_bug)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # top frame
        ttk.Label(self.top_frame, text="Timers:").pack(anchor="w")
        self.selected_timer = tkinter.StringVar(value="90 min" if self.default_option is None else self.default_option)
        self.timer_dropdown = ttk.Combobox(self.top_frame, textvariable=self.selected_timer,
                                           values=self.options,
                                           state="readonly", width=20)
        self.timer_dropdown.bind("<<ComboboxSelected>>", self.on_timer_select)
        self.timer_dropdown.pack(side="left")

        self.add_timer_button = ttk.Button(self.top_frame, text='+', command=self.add_timer, state='enabled')
        self.add_timer_button.pack(padx=3, side="left")

        # bottom frame
        self.start_button = ttk.Button(self.root, text='Start Timer', command=self.start_timer, state='enabled')
        self.start_button.pack(padx=3, pady=3, side="left")

        self.stop_button = ttk.Button(self.root, text='Stop Timer', command=self.cancel_timer, state='disabled')
        self.stop_button.pack(padx=3, pady=3, side="left")

        self.pause_button = ttk.Button(self.root, text='Pause Timer', command=self.pause_timer, state='disabled')
        self.pause_button.pack(padx=3, pady=3, side="left")

        self.root.bind('<Return>', self.start_timer)
        self.root.bind('<Alt_L>', self.show_config_menu)
        self.root.mainloop()

    def center_window(self, window):
        window.update_idletasks()

        # get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # get the current width and height of the window
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # center the window
        window.geometry(f"+{x}+{y}")

    def set_theme(self):
        # ensure theme is valid
        try:
            if self.theme != "light" and self.theme != "dark":
                self.theme = "dark"
                sv_ttk.set_theme(self.theme)
                self.prog.update_theme(theme=self.theme)
                raise ValueError("Theme must be either \"Light\" or \"Dark\".")

            # if valid theme, set to custom theme
            sv_ttk.set_theme(self.theme)
        except ValueError as e:
            tkinter.messagebox.showerror(
                "Invalid Theme",
                "Selected Theme is invalid, resetting theme to \"Dark\""
            )


    def start_timer(self, event=None):
        self.prog.start_timer(selection=self.selected_timer.get())
        if not self.running:
            duration, unit = self.selected_timer.get().split()

            if int(duration) > 0:
                self.running = True
                self.reinitialize_top_frame()
                self.toggle_start_stop_buttons()

    def cancel_timer(self):
        self.running = False
        self.paused = False
        self.reinitialize_top_frame()
        self.toggle_start_stop_buttons()
        self.prog.cancel_timer()

    def pause_timer(self):
        self.prog.pause_timer()
        self.paused = not self.paused
        self.toggle_start_stop_buttons()

    def add_timer(self):
        add_timer_gui = AddTimerGUI(parent=self.root, callback=self.save_timer)
        add_timer_gui.initialize_gui()

    def clear_timers(self):
        self.prog.clear_timers()
        self.options = self.prog.get_all_options()
        self.timer_dropdown["values"] = self.options

    def save_timer(self, duration, unit):
        self.prog.save_timer(duration=duration, unit=unit)
        self.options = self.prog.get_all_options()
        self.timer_dropdown["values"] = self.options

    def on_timer_select(self, event):
        self.timer_dropdown.selection_clear()

    def toggle_start_stop_buttons(self):
        if self.running and not self.paused:
            self.stop_button["state"] = "enabled"
            self.start_button["state"] = "disabled"
            self.pause_button["state"] = "enabled"
            self.pause_button["text"] = "Pause Timer"
        elif self.running and self.paused:
            self.stop_button["state"] = "enabled"
            self.start_button["state"] = "disabled"
            self.pause_button["state"] = "enabled"
            self.pause_button["text"] = "Unpause Timer"
        elif not self.running:
            self.stop_button["state"] = "disabled"
            self.start_button["state"] = "enabled"
            self.pause_button["state"] = "disabled"

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
        elif self.theme == "dark":
            self.theme = "light"
        else:
            self.theme = "dark"

        self.prog.update_theme(theme=self.theme)
        self.set_theme()

    def update_timer_display(self):
        time_remaining = self.prog.get_remaining_time()
        hours, minutes, seconds = map(int, time_remaining.split(':'))

        self.timer_display["state"] = "normal"
        self.timer_display.delete(0, "end")
        self.timer_display.insert(0, f"{time_remaining}")
        self.timer_display["state"] = "readonly"

        if (hours + minutes + seconds) <= 0:
            self.running = False
            self.reinitialize_top_frame()

    def reinitialize_top_frame(self):
        # clear top frame
        if self.timer_dropdown is not None:
            self.timer_dropdown.pack_forget()
        if self.timer_display is not None:
            self.timer_display.pack_forget()
        self.add_timer_button.pack_forget()

        # reinitialize top frame
        if self.running:
            # add timer display and re-add add button
            self.timer_display = ttk.Entry(self.top_frame, state="disabled", width=20)
            self.timer_display.pack(side="left")
            self.add_timer_button = ttk.Button(self.top_frame, text='+', command=self.add_timer, state='enabled')
            self.add_timer_button.pack(padx=3, side="left")

            # update timer
            self.update_timer_display()
        elif not self.running:
            # add timer dropdown and re-add add button
            self.selected_timer = tkinter.StringVar(
                value=self.selected_timer.get())
            self.timer_dropdown = ttk.Combobox(self.top_frame, textvariable=self.selected_timer,
                                               values=self.options,
                                               state="readonly", width=20)
            self.timer_dropdown.bind("<<ComboboxSelected>>", self.on_timer_select)
            self.timer_dropdown.pack(side="left")
            self.add_timer_button = ttk.Button(self.top_frame, text='+', command=self.add_timer, state='enabled')
            self.add_timer_button.pack(padx=3, side="left")

    def show_config_menu(self, event=None):
        self.root.config(menu=self.menu_bar)

    def feature_not_implemented_warning(self):
        tkinter.messagebox.showerror(
            "Still working on it!",
            "This feature isn't available yet. Check back soon!"
        )

    def github(self):
        url = "https://github.com/denemir/"
        webbrowser.open_new_tab(url)

    def report_bug(self):
        url = "https://github.com/denemir/Simple-Sleep-Timer/issues/new"
        webbrowser.open_new_tab(url)

    def resource(self, relative_path):
        import sys
        import os
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


class AddTimerGUI:
    def __init__(self, parent, callback):
        self.window = tkinter.Toplevel(parent)
        self.callback = callback

        # setup window
        self.window.title('Add Timer')
        self.window.minsize(200, 50)
        self.window.resizable(False, False)
        self.window.transient(parent)  # window modal
        self.window.grab_set()

        # inputs
        self.duration_frame = None
        self.duration_input = None
        self.duration_units = None
        self.unit = None

    def initialize_gui(self):
        top_frame = ttk.Frame(self.window)
        top_frame.pack(padx=3, pady=3, side="top", fill="x")
        self.center_window(self.window)

        # input
        self.duration_frame = ttk.Frame(top_frame)
        self.duration_frame.pack(padx=3, pady=3, side="left")
        validation = (self.window.register(self.validate_input), "%P") # input validation

        ttk.Label(self.duration_frame, text="Duration:").pack(anchor="w")
        self.duration_input = ttk.Entry(self.duration_frame, width=30, validate="key", validatecommand=validation)
        self.duration_input.pack()

        # units
        self.unit = tkinter.StringVar(value="min")
        unit_frame = ttk.Frame(top_frame)
        unit_frame.pack(padx=3, side="left")

        ttk.Label(unit_frame, text="Units:").pack(anchor="w")
        self.duration_units = ttk.Combobox(unit_frame, textvariable=self.unit,
                                           values=["sec", "min", "hrs"],
                                           state="readonly", width=4)
        self.duration_units.bind("<<ComboboxSelected>>", self.on_dropdown_select)
        self.duration_units.pack(side="right", padx=3)

        save_button = ttk.Button(self.window, text='Save', command=self.save_timer, state='enabled')
        save_button.pack(side="bottom", pady=3)

    def center_window(self, window):
        # get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # get the current width and height of the window
        window.update_idletasks()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # center the window
        window.geometry(f"+{x}+{y}")

    def on_dropdown_select(self, event):
        self.duration_units.selection_clear()

    def save_timer(self):
        try:
            duration = self.duration_input.get().strip()
            unit = self.unit.get().strip()
            if float(self.duration_input.get()) <= 0:
                raise ValueError("Duration must be positive")

            # Call the callback with the new timer info
            self.callback(duration, unit)
            self.window.destroy()

        except ValueError as e:
            tkinter.messagebox.showerror(
                "Invalid Input",
                "Please enter a valid positive number for duration."
            )

    def validate_input(self, P):
        return P.isdigit() or P == ''
