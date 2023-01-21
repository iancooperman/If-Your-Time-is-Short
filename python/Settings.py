import json
from pathlib import Path


class Settings:
    """
    This is a singleton class that manages the dictionary representation of a JSON settings file.

    Attributes:
    _instance (Settings): The singleton instance of this class.
    _settings_dict (dict): The dictionary representation of the JSON settings file.

    Methods:
    __new__(cls): Ensures that only one instance of this class is created by checking if an instance already exists and returning it if it does.

    load_settings(self, settings_file_path: str) -> None: Accepts a file path, opens the file and loads its contents as a JSON object to the settings dictionary.

    save_settings(self, settings_file_path: str) -> None: Accepts a file path and saves the contents of the settings dictionary to the specified file.

    __getitem__(self, key: str) -> Any: Returns the value of the specified key in the loaded JSON object.

    __setitem__(self, key: str, value: Any) -> None: Sets the value of the specified key to the specified value in the loaded JSON object.

    __str__(self) -> str: Returns a string representation of the settings dictionary with indentation of 4 spaces.

    __repr__(self) -> str: Returns a string representation of the settings dictionary.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def load_settings(self, settings_file_path: str):
        with open(settings_file_path, 'r') as f:
            self._settings_dict = json.load(f)

    def save_settings(self, settings_file_path: str):
        with open(settings_file_path, "w") as f:
            json.dump(self._settings_dict, f, indent=4)

    def __getitem__(self, item: str):
        if item in self._settings_dict:
            return self._settings_dict[item]
        else:
            raise KeyError(item)

    def __setitem__(self, key: str, value: str):
        self._settings_dict[key] = value

    def __str__(self):
        return json.dumps(self._settings_dict, indent=4)

    def __repr__(self):
        return repr(self._settings_dict)


if __name__ == '__main__':
    settings_file_path = Path(str(Path(__file__).parents[0]) + "/../settings.json")
    settings = Settings()
    settings.load_settings(settings_file_path)
    print(settings)
    settings["reddit_secret"] = "secret"
    settings.save_settings(settings_file_path)