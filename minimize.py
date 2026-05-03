import pystray
from PIL import Image, ImageDraw
import threading

class Minimize:
    @staticmethod
    def create_tray_icon_image():
        return Image.open("icon.png").resize((32, 32))

    @staticmethod
    def build_tray_icon(app):
        menu = pystray.Menu(
            pystray.MenuItem("Show", lambda: app.restore_from_tray()),
            pystray.MenuItem("Quit", lambda: app.quit())
        )
        icon = pystray.Icon("SimpleSleepTimer", app.create_tray_icon_image(), "Simple Sleep Timer", menu)
        app.tray_icon = icon
        icon.run()

    @staticmethod
    def minimze_to_tray(app):
        app.root.withdraw()
        thread = threading.Thread(target=Minimize.build_tray_icon, args=(app,), daemon=True)
        thread.start()

    @staticmethod
    def restore_from_tray(app):
        if hasattr(app, 'tray_icon'):
            app.tray_icon.stop()
        app.root.deiconify()
        app.root.lift()