import threading
import datetime
import time

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

    def restart(self):
        self.stop()
        self.start()

    def _run(self):
        fired_today = None

        while not self._stop_event.is_set():
            try:
                if self.config.get_scheduled():
                    schedule = self.config.get_schedule()
                    now = datetime.datetime.now()
                    current_day = now.strftime("%A")
                    current_time = now.strftime("%H:%M")
                    today = now.date()

                    days = schedule.get("days", [])
                    sleep_at = schedule.get("sleep_at", "")

                    should_fire = (
                        current_day in days and
                        current_time == sleep_at and
                        fired_today != today
                    )

                    if should_fire:
                        fired_today = today
                        self.sleep_callback()

            except Exception as e:
                print(f"Scheduler error: {e}")

            time.sleep(30)