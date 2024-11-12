from dotenv import load_dotenv
from src.constant import REPO_ROOT


def loadenv():
    load_dotenv()
    load_dotenv(REPO_ROOT/'public.env')
    