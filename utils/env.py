import os

from dotenv import load_dotenv

load_dotenv()


def str_env(variable: str) -> str | None:
    return os.environ.get(variable)


def int_env(variable: str) -> int:
    return int(os.environ.get(variable, 3))
