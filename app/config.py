from dataclasses import dataclass
from os import environ


@dataclass
class Config:

    version = "v.0.1.0"
    token = environ['TOKEN']        # You need to add an environment variable
    database = environ['DATABASE']  # Your database name
    username = environ['USER']      # Your database username
    password = environ['PASSWORD']  # Your database password
    host = environ['HOST']          # Your database host
