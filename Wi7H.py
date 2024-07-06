from dotenv import load_dotenv
from langchain_upstage import UpstageEmbeddings
from langchain_upstage import ChatUpstage
from langchain_core.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI
from pprint import pprint
#from langchain_chroma import Chroma DB -> chroma vs oracleVS
import os
import oracledb
import warnings

warnings.filterwarnings("ignore")

def initialize():
    load_dotenv()
    client = OpenAI(
        api_key=os.environ.get('UPSTAGE_API_KEY'), base_url="https://api.upstage.ai/v1/solar"
    )
    return client

def first_qna():

def 

if __name__=="__main__":
    client = initialize()

    first_qna()
