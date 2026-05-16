import pystray
from PIL import Image, ImageDraw
import threading

from gui_common import GuiCommon


class Minimize:
    @staticmethod
    def create_tray_icon_image():
        icon_path = GuiCommon.resource_path("icon.png")
        return Image.open(icon_path).resize((32, 32))

    @staticmethod
    def build_tray_icon(app):
        menu = pystray.Menu(
            pystray.MenuItem("Show", lambda icon, item: Minimize.restore_from_tray(app)),
            pystray.MenuItem("Quit", lambda icon, item: Minimize.quit_from_tray(app))
        )
        icon = pystray.Icon("SimpleSleepTimer", Minimize.create_tray_icon_image(), "Simple Sleep Timer", menu)
        app.tray_icon = icon
        icon.run()

    @staticmethod
    def minimize_to_tray(app):
        app.root.withdraw()
        thread = threading.Thread(target=Minimize.build_tray_icon, args=(app,), daemon=True)
        thread.start()

    @staticmethod
    def restore_from_tray(app):
        if hasattr(app, 'tray_icon'):
            app.tray_icon.stop()
        app.root.deiconify()
        app.root.lift()

    @staticmethod
    def quit_from_tray(app):
        if hasattr(app, 'tray_icon'):
            app.tray_icon.stop()
        app.root.destroy()

    @staticmethod
    def on_close(app, behavior=None):
        if behavior == "tray":
            Minimize.minimize_to_tray(app)
        elif behavior == "quit":
            app.root.destroy()
