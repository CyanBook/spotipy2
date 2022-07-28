from __future__ import annotations
from typing import Type
import inspect


class BaseType:
    @classmethod
    def from_dict(cls, json: dict) -> Type[BaseType]:
        if "_id" in json:  # MongoDB _id parameter
            json.pop("_id")

        try:
            return cls(**json)
        except TypeError:
            # Remove unwanted parameter(s)
            class_keys = inspect.signature(cls).parameters.keys()
            new_json = {k: v for k, v in json.items() if k in class_keys}

            # Return the new class without any extra parameter
            return cls(**new_json)
