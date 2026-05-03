import json
import logging
import os


class Config:
    def __init__(self, config_path="settings.json"):
        self.config_path = config_path
        self.default_config = {
            "timers": {},
            "scheduled_times": {},
            "preferences": {
                "default_option": None,
                "theme": "dark",
                "notifications": False,
                "minimize_on_close": False,
                "run_on_startup": False,
                "scheduled": False,
            },
        }
        self.version = '1.0.2'
        self.config = self.load_config()

    def load_config(self):
        try:
            config = None
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
            else:
                self.save_config(self.default_config)
                config = self.default_config

            return config

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

    def delete_timers(self):
        self.config["timers"] = {}
        self.save_config(self.config)

    def set_default_option(self, duration, unit):
        timer_title = f'{duration} ' + f'{unit}'
        self.config["preferences"]["default_option"] = timer_title
        self.save_config(self.config)

    def get_timers(self):
        return self.config["timers"]

    def get_default_option(self):
        return self.config["preferences"]["default_option"]

    def get_theme(self):
        return self.config["preferences"]["theme"]

    def set_theme(self, theme=None):
        self.config["preferences"]["theme"] = theme
        self.save_config(self.config)

    def set_run_on_startup(self, option=None):
        self.config["preferences"]["run_on_startup"] = option
        self.save_config(self.config)

    def set_minimize_on_close(self, option=None):
        self.config["preferences"]["minimize_on_close"] = option
        self.save_config(self.config)

    def get_minimize_on_close(self):
        return self.config["preferences"]["minimize_on_close"]

    def set_scheduled(self, option=None):
        self.config["preferences"]["scheduled"] = option
        self.save_config(self.config)

    def get_scheduled(self):
        return self.config["preferences"]["scheduled"]

    def add_schedule(self, schedules=None):
        self.config["scheduled_times"] = schedules
        self.save_config(self.config)
