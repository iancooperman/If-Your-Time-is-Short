import json
from pathlib import Path


class Settings:
    def __init__(self, settings_file_path: str):
        with open(settings_file_path, 'r') as f:
            self._settings_dict = json.load(f)

    def __getattr__(self, item: str):
        if item in self._settings_dict:
            return self._settings_dict[item]
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, item))


if __name__ == '__main__':
    settings_file_path = Path(str(Path(__file__).parents[0]) + "/../settings.json")
    settings = Settings(settings_file_path)
    print(settings.OPENAI_API_KEY)