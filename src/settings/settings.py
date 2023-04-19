import os
import json
from typing import Dict, Any


class Settings:
    def __init__(self, root_dir: str = None):
        if root_dir is None:
            # default to ~/.tinmind
            self.root_dir = os.path.join(os.path.expanduser("~"), ".tinmind")
        else:
            self.root_dir = root_dir
        self.settings_file = os.path.join(self.root_dir, "settings.json")

        self._load_settings()

    def _load_settings(self):
        # load setings from settings file
        # create the path if it doesnt exist

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
        if os.path.exists(self.settings_file):
            with open(self.settings_file) as f:
                self.settings = json.load(f)
        else :
            self.settings = {}

    def get(self, key: str) -> Any:
        if key not in self.settings:
            return None
        return self.settings[key]
    
    def set(self, key: str, value: Any):
        self.settings[key] = value
        self._save_settings()
    
    def _save_settings(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)
