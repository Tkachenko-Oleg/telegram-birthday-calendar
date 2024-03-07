from dataclasses import dataclass
from os import environ


@dataclass
class Config:

    token = environ['TOKEN']                # You need to add an environment variable
    api_id = environ['API_ID']              # You need to add an environment variable
    api_hash = environ['API_HASH']          # You need to add an environment variable
