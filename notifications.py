from winotify import Notification, audio
import os
import sys

APP_NAME = "Simple Sleep Timer"
APP_ID = "SimpleSleepTimer"

class Notifications:
    @staticmethod
    def get_icon_path():
        base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "icon.ico")
        return path if os.path.exists(path) else ""

    @staticmethod
    def _send(title: str, message: str, sound=audio.Default, duration="Short"):
        toast = Notification(
            app_id=APP_ID,
            title=title,
            msg=message,
            duration=duration,
            icon=Notifications.get_icon_path()
        )
        toast.set_audio(sound, loop=False)
        toast.show()

    @staticmethod
    def notify_running_in_background():
        Notifications._send(
            title=f"{APP_NAME} is running",
            message="The app is running in the background.",
            sound=audio.Default,
            duration="Short"
        )

    @staticmethod
    def notify_schedule_warning():
        Notifications._send(
            title="Sleep in 5 minutes",
            message="Your scheduled sleep time is coming up in 5 minutes.",
            sound=audio.Reminder,
            duration="Long"
        )

    @staticmethod
    def notify_custom_timer_warning(seconds_remaining: int):
        minutes = seconds_remaining // 60
        seconds = seconds_remaining % 60
        time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        Notifications._send(
            title="Sleep Timer Warning",
            message=f"Your system will sleep in {time_str}.",
            sound=audio.Reminder,
            duration="long"
        )