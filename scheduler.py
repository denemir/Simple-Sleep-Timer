import threading
import datetime
import time

from notifications import Notifications


class Scheduler:
    def __init__(self, config, sleep_callback):
        self.config = config
        self.sleep_callback = sleep_callback
        self._thread = None
        self._stop_event = threading.Event()

    def start(self):
        # already running
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()

    def restart(self):
        self.stop()
        self.start()

    def _run(self):
        fired_today = None
        warning_sent_today = None # tracker for notification warning

        while not self._stop_event.is_set():
            try:
                if self.config.get_scheduled():
                    schedule = self.config.get_schedule()
                    now = datetime.datetime.now()
                    current_day = now.strftime("%A")
                    today = now.date()

                    days = schedule.get("days", [])
                    sleep_at = schedule.get("sleep_at", "")

                    if current_day in days and sleep_at:
                        sleep_hour, sleep_minute = map(int, sleep_at.split(":"))
                        sleep_time = now.replace(hour=sleep_hour, minute=sleep_minute, second=0, microsecond=0)
                        delta = (sleep_time - now).total_seconds()

                        if 270 <= delta <= 330 and warning_sent_today != today:
                            if self.config.get_enable_notifications():
                                warning_sent_today = today
                                Notifications.notify_schedule_warning()

                        if -30 <= delta <= 30 and fired_today != today:
                            fired_today = today
                            self.sleep_callback()

            except Exception as e:
                print(f"Scheduler error: {e}")

            time.sleep(5)