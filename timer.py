import threading
from threading import Event
import time
import re
import tkinter
from tkinter import messagebox


class Timer:
    def __init__(self, callback=None, update_call=None):
        self.duration = 0
        self.time_remaining = 0
        self.paused = False
        self.running = False
        self.thread = None
        self.callback = callback
        self.update_call = update_call

        # thread
        self._pause_event = Event()
        self._stop_event = Event()

    def start_timer(self, selection=None, on_complete=None):
        self.callback = on_complete
        self.duration = self.parse_duration(selection=selection)
        self.paused = False
        self._stop_event.clear()
        self._pause_event.clear()

        # check to ensure time was properly parsed
        if self.duration is not None:
            self.time_remaining = self.duration
            self.running = True

            # start thread
            self.thread = threading.Thread(target=self._decrement)
            self.thread.daemon = True
            self.thread.start()
        else:
            self.duration = 0
            return

    def set_timer(self, duration=None):
        self.duration = duration

    def pause_timer(self):
        if self.paused:
            self._pause_event.clear()
        else:
            self._pause_event.set()
        self.paused = not self.paused

    def cancel_timer(self):
        self._stop_event.set()
        self._pause_event.clear()
        self.paused = False
        self.time_remaining = 0
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.001)

    def get_remaining_time(self):
        hours = self.time_remaining // 3600
        minutes = (self.time_remaining % 3600) // 60
        seconds = self.time_remaining % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_remaining_time_in_seconds(self):
        return self.time_remaining

    def parse_duration(self, selection=None):
        # check format
        try:
            match = re.match(r"(\d+)\s*(min|hrs?|sec)", selection.lower())
            if not match:
                raise ValueError(f"Invalid duration format: {selection}")
        except ValueError as e:
            tkinter.messagebox.showerror(
                "Invalid Input",
                "Please enter a valid time in this format: { Duration } { Units }"
            )
            return None

        # parse values
        duration, unit = match.groups()
        duration = int(duration)

        # convert to seconds
        if unit.startswith("hr"):
            return duration * 3600
        elif unit == "min":
            return duration * 60
        elif unit == "sec":
            return duration
        else:
            raise ValueError(f"Invalid unit format: {selection}")

    def _decrement(self):
        while self.running and self.time_remaining > 0:
            # check for pause
            if self._pause_event.is_set():
                continue

            if self._stop_event.is_set() or self._pause_event.is_set():
                break
            time.sleep(1)

            if not self._stop_event.is_set() and not self._pause_event.is_set():
                self.time_remaining -= 1
                self.update_call()

            if self.time_remaining <= 0 and self.running:
                if self.callback:
                    self.running = False
                    self.callback()
                break
