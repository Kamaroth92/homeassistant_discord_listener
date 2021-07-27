import os
from dotenv import load_dotenv

load_dotenv(override=False)
def return_var(envvar):
    return os.environ.get(envvar)