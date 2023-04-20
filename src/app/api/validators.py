import json

import phonenumbers
from pydantic import BaseModel
from pydantic.validators import strict_str_validator


class PhoneNumber(str):
    @classmethod
    def __get_validators__(cls):
        yield strict_str_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        v = v.strip().replace(" ", "")

        try:
            pn = phonenumbers.parse(v)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Invalid phone number format")

        return cls(phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164))


class JSONValidator(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
