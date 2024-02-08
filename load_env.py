"""Loads env file (only for production)"""
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALG = os.getenv("ALG")
