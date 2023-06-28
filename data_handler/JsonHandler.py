import dataclasses
import json


class JsonHandler:
    class JSONEncoderForDataclass(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

    def __init__(self):
        pass

    def return_json_as_dict(self, json_path: str) -> dict:
        with open(json_path, "r", encoding="utf-8") as json_file:
            json_file = json_file.read()
            return json.loads(json_file)

    def save_json(self, json_path: str, data: dict) -> None:
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(
                data,
                json_file,
                indent=4,
                ensure_ascii=False,
                cls=self.JSONEncoderForDataclass,
            )
