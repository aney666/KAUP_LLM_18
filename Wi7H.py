from dotenv import load_dotenv
from langchain_upstage import UpstageEmbeddings
from openai import OpenAI
from pprint import pprint
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings
from langchain_upstage import UpstageEmbeddings

import os
import oracledb
import warnings

warnings.filterwarnings("ignore")

def initialize():
    load_dotenv()
    client = OpenAI(
        api_key=os.environ.get('UPSTAGE_API_KEY'), base_url="https://api.upstage.ai/v1/solar"
    )


def prompting():
