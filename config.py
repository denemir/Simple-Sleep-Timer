import json
import os


class Config:
    def __init__(self, config_path="settings.json"):
        self.config_path = config_path
        self.default_config = {
            "timers": {},
            "default_option": None,
            "theme": "dark"
        }
        self.version = '1.0.1'
        self.config = self.load_config()

    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                self.save_config(self.default_config)
                return self.default_config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            return self.default_config

    def save_config(self, config_data):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=4)
            self.config = config_data
        except IOError as e:
            print(f"Error saving config: {e}")

    def add_timer(self, duration, unit):
        timer_title = f"{duration} {unit}"
        self.config["timers"][timer_title] = {
            "duration:": duration,
            "unit:": unit
        }
        self.save_config(self.config)

    def set_default_option(self, duration, unit):
        timer_title = duration, unit
        self.config["default_option"][timer_title] = {
            "duration:": duration,
            "unit:": unit
        }
        self.save_config(self.config)

    def get_timers(self):
        return self.config["timers"]

    def get_default_option(self):
        return self.config["default_option"]

    def get_theme(self):
        return self.config["theme"]

    def set_theme(self, theme=None):
        self.config["theme"] = theme
        self.save_config(self.config)
