# Example of hard code of login

from pathlib import Path
from dotenv import load_dotenv
import os

CURRENT_DIR = Path(__file__).resolve().parent
load_dotenv(CURRENT_DIR / "script.env")
user = os.getenv("user")
pasword = os.getenv("pasword")
key = os.getenv("key")
session = os.getenv("session")
token = os.getenv("token")


def connect(user, pswd):
    print(f"{user} {pswd}")


connect(user, pasword)
