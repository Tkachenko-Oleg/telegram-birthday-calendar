from dataclasses import dataclass
from os import environ


@dataclass
class Config:

    version = "v.0.4.0"
    token = environ['TOKEN']                # You need to add an environment variable
    database = environ['DATABASE']          # Your database name
    username = environ['USERDATABASE']      # Your database username
    password = environ['PASSWORD']          # Your database password
    host = environ['HOST']                  # Your database host
    port = environ['PORT']                  # Your database port
