import yaml
from pathlib import Path

# class Config:

#     def get(self, item: str):
#         if item in self.data:
#             return self.data[item]
#         else:
#             raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, item))

#     def fromYAML(self, yaml_file_path: str):
#         with open(yaml_file_path, 'r') as f:
#             self.data = yaml.load(f)

# javax.json inspired YAML parser
class YAMLObject:
    def __init__(self, data: dict) -> None:
        self._data = data
    
    @classmethod
    def from_string(cls, string: str):
        data = yaml.load(string, Loader=yaml.FullLoader)

        return cls(data)

    @classmethod
    def from_file_stream(cls, fs):
        return cls.from_string(fs.read())

    @classmethod 
    def from_dict(cls, data: dict):
        return cls(data)

    def get_object(self, key: str):
        if key in self._data and isinstance(self._data[key], dict):
            return YAMLObject.from_dict(self._data[key])

    def get_list(self, key: str):
        if key in self._data and isinstance(self._data[key], list):
            return [YAMLObject.from_dict(item) for item in self._data[key]]

    def get_value(self, key: str):
        if key in self._data:
            return self._data[key]



    
    
    def __str__(self):
        return yaml.dump(self._data, default_flow_style=False)

    def __repr__(self) -> str:
        return str(self._data)

class YAMLList:
    def __init__(self, data: list) -> None:
        self._data = data


        

    


# _config_file_path = Path(str(Path(__file__).parents[0]) + "/../config.yaml")
# CONFIG = Config(_config_file_path)

if __name__ == '__main__':
    config_file_path = Path(str(Path(__file__).parents[0]) + "/../config.yaml")
    yaml_object = YAMLObject.from_dict({
        "hi": "world"
    })
    print(yaml_object)
