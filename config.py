import json
import os
import shutil
import sys
import zipfile

import requests

from updater_gui import UpdaterGui


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
                "startup_in_background": False,
                "scheduled": False,
                "online_updater": True
            },
        }
        self.version = '1.1.0'
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

    def get_run_on_startup(self):
        return self.config["preferences"]["run_on_startup"]

    def set_startup_in_background(self, option=None):
        self.config["preferences"]["startup_in_background"] = option
        self.save_config(self.config)

    def get_startup_in_background(self):
        return self.config["preferences"]["startup_in_background"]

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

    def set_schedule(self, schedule: dict):
        self.config["scheduled_times"] = {
            "days": schedule["days"],
            "sleep_at": schedule["sleep_at"]
        }
        self.save_config(self.config)

    def get_schedule(self) -> dict:
        return {
            "days": self.config["scheduled_times"].get("days", []),
            "sleep_at": self.config["scheduled_times"].get("sleep_at", "22:00")
        }

    def set_enable_notifications(self, option=None):
        self.config["preferences"]["notifications"] = option
        self.save_config(self.config)

    def get_enable_notifications(self):
        return self.config["preferences"]["notifications"]

    def set_enable_online_updater(self, option=None):
        self.config["preferences"]["online_updater"] = option
        self.save_config(self.config)

    def get_enable_online_updater(self):
        return self.config["preferences"]["online_updater"]

    def get_preference(self, preference=None):
        return self.config["preferences"][f"{preference}"]

    def set_preference(self, preference=None, option=None):
        self.config["preferences"][f"{preference}"] = option
        self.save_config(self.config)

    def check_for_update(self):
        repo_link = "https://github.com/denemir/Simple-Sleep-Timer/releases/latest"
        response = requests.get(repo_link)

        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release["tag_name"]

            if latest_version != self.version:
                UpdaterGui.initialize_window(config=self.config, latest_version=latest_version)

    def update_application(self, download_url):
        response = requests.get(download_url)
        if response.status_code == 200:
            with open("update.zip", "wb") as file:
                file.write(response.content)

            with zipfile.ZipFile("update.zip", "r") as zip_ref:
                zip_ref.extractall("update")

            existing_settings = self.load_config()

            current_path = os.path.dirname(os.path.abspath(__file__))
            update_path = os.path.join(current_path, "update")

            for filename in os.listdir(current_path):
                if filename != "settings.json":
                    file_path = os.path.join(current_path, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)

            for filename in os.listdir(update_path):
                src_path = os.path.join(update_path, filename)
                dst_path = os.path.join(current_path, filename)
                if os.path.isfile(src_path):
                    shutil.copy(src_path, dst_path)
                elif os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path)

            os.remove("update.zip")
            shutil.rmtree("update")

            updated_settings = self.load_config()
            merged_settings = {**updated_settings, **existing_settings}
            self.save_config(merged_settings)

            # reset the application
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            print("Failed to download the update.")

    def merge_missing_config_attributes(self):
        self.config = self.merge_dicts(self.default_config, self.config)
        self.save_config(self.config)

    def merge_dicts(self, default_dict, user_dict):
        merged_dict = {}
        for key in default_dict:
            if key in user_dict:
                if isinstance(default_dict[key], dict) and isinstance(user_dict[key], dict):
                    merged_dict[key] = self.merge_dicts(default_dict[key], user_dict[key])
                else:
                    merged_dict[key] = user_dict[key]
            else:
                merged_dict[key] = default_dict[key]
        return merged_dict
