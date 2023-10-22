from dataclasses import dataclass
from os import environ


@dataclass
class Config:

    version = "v.0.0.2"
    token = environ['TOKEN']    # You need to add an environment variable
