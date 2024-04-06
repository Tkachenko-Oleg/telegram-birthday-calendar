from dataclasses import dataclass
from os import environ


@dataclass
class Config:

    token = environ['TOKEN']
    api_id = environ['API_ID']
    api_hash = environ['API_HASH']
    database = environ['DATABASE']
    username = environ['USERDATABASE']
    password = environ['PASSWORD']
    host = environ['HOST']
    port = environ['PORT']
