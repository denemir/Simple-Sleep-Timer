import tkinter
from tkinter import ttk

from gui_common import GuiCommon

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
HOURS = [f"{h:02d}" for h in range(0,24)]
MINUTES = [f"{m:02d}" for m in range(0, 60, 5)]

class SchedulerGui:
    def __init__(self, parent, config, callback):
        self.window = tkinter.Toplevel(parent)
        self.window.focus_force()
        self.callback = callback
        self.config = config

        # setup window
        self.window.title('Scheduler')
        self.window.minsize(200, 50)
        self.window.resizable(True, True)
        self.window.transient(parent)  # window modal
        self.window.grab_set()
        self.content_frame = None

        # sleep vars
        self.schedule = self.config.get_schedule() if self.config else {}
        self.day_vars = {
            day: tkinter.BooleanVar(value=day in self.schedule.get("days", []))
            for day in DAYS
        }
        self.sleep_at = self.schedule.get("sleep_at", "22:00").split(":")
        self.sleep_hour = tkinter.StringVar(value=self.sleep_at[0])
        self.sleep_minute = tkinter.StringVar(value=self.sleep_at[1])

        self.scheduler_enabled = tkinter.BooleanVar(value=self.config.get_scheduled())

    def initialize_gui(self):
        top_frame = ttk.Frame(self.window)
        top_frame.pack(padx=3, pady=3, side="top", fill="x")
        GuiCommon.center_window(self.window)

        # warning banner
        warning = ttk.Label(top_frame, text="'Run on startup' must be enabled in Preferences in order to use the Scheduler.",
                            foreground="red", font=("Arial", 8))
        warning.pack()

        # render fields
        self.render_enable_field_and_sleep_at()
        self.content_frame = ttk.Frame(self.window)
        self.content_frame.pack(fill="x", padx=10, pady=10)
        self.render_date_boxes(self.content_frame)
        self.render_save_button(self.content_frame)

    def render_enable_field_and_sleep_at(self):
        top_bar = ttk.Frame(self.window)
        top_bar.pack(fill="x", padx=10, pady=(5, 0))
        self.render_enable_field(top_bar)
        self.render_sleep_at(top_bar)

    def render_enable_field(self, frame):
        ttk.Checkbutton(
            frame, text="Enable Schedule",
            variable=self.scheduler_enabled,
            command=self.on_toggle_schedule
        ).pack(side="left")

    def render_sleep_at(self, frame):
        ttk.Label(frame, text="Sleep at: ").pack(side="left", padx=(20, 4))

        picker_frame = ttk.Frame(frame)
        picker_frame.pack(anchor="w")

        hour_box = ttk.Combobox(picker_frame, textvariable=self.sleep_hour,
                                values=HOURS, width=4, state="readonly")
        hour_box.pack(side="left")

        ttk.Label(picker_frame, text=":").pack(side="left", padx=2)

        minute_box = ttk.Combobox(picker_frame, textvariable=self.sleep_minute,
                                  values=MINUTES, width=4, state="readonly")
        minute_box.pack(side="left")

        ttk.Label(picker_frame, text="(24hr)").pack(side="left", padx=(6, 0))

    def render_date_boxes(self, window):
        days_label = ttk.Label(window, text="Active Days")
        days_label.pack(anchor="w", pady=(0, 4))

        grid = ttk.Frame(window)
        grid.pack(anchor="w")

        for i, day in enumerate(DAYS):
            ttk.Checkbutton(
                grid, text=day, variable=self.day_vars[day]
            ).grid(row=i // 4, column=i % 4, sticky="w", padx=6, pady=2)

    def render_save_button(self, window):
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(btn_frame, text="Save", command=self.on_save).pack(side="right")

    def on_toggle_schedule(self):
        state = tkinter.NORMAL if self.scheduler_enabled.get() else tkinter.DISABLED
        for widget in self.content_frame.winfo_children():
            try:
                widget.config(state=state)
            except tkinter.TclError:
                pass

    def on_save(self):
        schedule = self.get_schedule()
        if self.config:
            self.config.set_schedule(schedule)
            self.config.set_scheduled(self.scheduler_enabled.get())

        self.window.destroy()

    def get_schedule(self):
        return {
            "days": [day for day, var in self.day_vars.items() if var.get()],
            "sleep_at": f"{self.sleep_hour.get()}:{self.sleep_minute.get()}"
        }