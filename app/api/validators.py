import json
from pydantic import model_validator


class JSONValidatorMixin:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
