import copy
import re
from dataclasses import dataclass as python_dataclass
from typing_extensions import Annotated

from pydantic import ValidationError
from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic.functional_validators import BeforeValidator

sample_input_1 = {
    "name": "Jeremy",
    "age": 42,
    "percentile": ">99",
}

sample_input_2 = {
    "name": "Mary",
    "age": 42,
    "percentile": "64",
}

sample_input_3 = {
    "name": "Mary",
    "age": "24 years, 6 months",
    "percentile": "32nd",
}


#
# Python dataclass with parse_input function
#
@python_dataclass
class Ctopp:
    name: str
    age: int
    percentile: str


def parse_int(value: int | float | str) -> int:
    try:
        return int(value)
    except ValueError:
        age_match = re.match(r"(\d+)", value)
        if age_match:
            return int(age_match.group(1))
    raise ValidationError(f"value unable to be converted to int: {value}")


def parse_percentile(percentile: str | int | float) -> str:
    # Convert the input to int if it's not already
    if not isinstance(percentile, (int, float)):
        if percentile == "<1" or percentile == ">99":
            return percentile
        try:
            percentile = int(percentile)
        except ValueError:
            percentile_match = re.match(r"(\d+)", percentile)
            if percentile_match:
                percentile = int(percentile_match.group(1))
            else:
                raise ValueError("Invalid percentile format")

    # Convert percentile to string based on the specified rules
    if percentile < 1:
        return "<1"
    elif percentile > 99:
        return ">99"
    else:
        return str(int(percentile))


def parse_input(input: dict) -> Ctopp:
    results = copy.deepcopy(input)
    for key, value in input.items():
        if key == "age":
            results[key] = parse_int(value)
        elif key == "percentile":
            results[key] = parse_percentile(value)
    return Ctopp(**results)


print("\nPython with parse_input")
python_1 = parse_input(sample_input_1)
print(python_1)
python_2 = parse_input(sample_input_2)
print(python_2)
python_3 = parse_input(sample_input_3)
print(python_3)


#
# Python dataclass with __post_init__
#
@python_dataclass
class CtoppPython:
    name: str
    age: int
    percentile: str

    def __post_init__(self):
        self.age = self.parse_age(self.age)
        self.percentile = self.parse_percentile(self.percentile)

    def parse_age(self, age: int | float | str) -> int:
        try:
            return int(age)
        except ValueError:
            age_match = re.match(r"(\d+)", age)
            if age_match:
                return int(age_match.group(1))
        raise ValueError(f"age unable to be converted to int: {age}")

    def parse_percentile(self, percentile: str | int | float) -> str:
        if percentile == "<1" or percentile == ">99":
            return percentile

        # Convert the input to int if it's not already
        if not isinstance(percentile, (int, float)):
            try:
                percentile = int(percentile)
            except ValueError:
                percentile_match = re.match(r"(\d+)", percentile)
                if percentile_match:
                    percentile = int(percentile_match.group(1))
                else:
                    raise ValueError("Invalid percentile format")

        # Convert percentile to string based on the specified rules
        if percentile < 1:
            return "<1"
        elif percentile > 99:
            return ">99"
        else:
            return str(int(percentile))


print("\nPython dataclass")
python_1 = CtoppPython(**sample_input_1)
print(python_1)
python_2 = CtoppPython(**sample_input_2)
print(python_2)
python_3 = CtoppPython(**sample_input_3)
print(python_3)


#
# Pydantic dataclass
#
def validate_age(age: int | float | str) -> int:
    try:
        return int(age)
    except ValueError:
        age_match = re.match(r"(\d+)", age)
        if age_match:
            return int(age_match.group(1))
    raise ValidationError(f"age unable to be converted to int: {age}")


def validate_percentile(percentile: str | int | float) -> str:
    if percentile == "<1" or percentile == ">99":
        return percentile

    # Convert the input to int if it's not already
    if not isinstance(percentile, (int, float)):
        try:
            percentile = int(percentile)
        except ValueError:
            percentile_match = re.match(r"(\d+)", percentile)
            if percentile_match:
                percentile = int(percentile_match.group(1))
            else:
                raise ValueError("Invalid percentile format")

    # Convert percentile to string based on the specified rules
    if percentile < 1:
        return "<1"
    elif percentile > 99:
        return ">99"
    else:
        return str(int(percentile))


Age = Annotated[int, BeforeValidator(validate_age)]
Percentile = Annotated[str, BeforeValidator(validate_percentile)]


@pydantic_dataclass
class CtoppPydantic:
    name: str
    age: Age
    percentile: Percentile


print("\nPydantic dataclass")
pydantic_1 = CtoppPydantic(**sample_input_1)
print(pydantic_1)
pydantic_2 = CtoppPydantic(**sample_input_2)
print(pydantic_2)
pydantic_3 = CtoppPydantic(**sample_input_3)
print(pydantic_3)
