from dotenv import load_dotenv
from langchain_upstage import UpstageEmbeddings
from langchain_upstage import ChatUpstage
from langchain_core.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import LLMChain
from langchain_core.documents import BaseDocumentTransformer, Document
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.vectorstores import oraclevs
from langchain_community.vectorstores.oraclevs import OracleVS
from openai import OpenAI
from pprint import pprint

import os
import sys
import array
import time
import oracledb
import warnings

warnings.filterwarnings("ignore")

Char_list = ["""
    
    당신의 MBTI는 무엇입니까?
    ISTP
    직무와 관련해, 어떤 역할을 맡고 싶나요?
    개발자
    당신의 커리어는 어떻게 되나요?
    유니스트 재학중
    직무와 관련해, 당신의 관심사는 무엇인가요?
    NLP
    당신의 업무철학은 어떻게 되나요?
    돈

    """,
    """
    당신의 MBTI는 무엇입니까?
    ISFJ
    직무와 관련해, 어떤 역할을 맡고 싶나요?
    디자이너
    당신의 커리어는 어떻게 되나요?
    업스테이지 로고 개발
    직무와 관련해, 당신의 관심사는 무엇인가요?
    로고개발
    당신의 업무철학은 어떻게 되나요?
    돈
    """,
    """
    당신의 MBTI는 무엇입니까?
    INTJ
    직무와 관련해, 어떤 역할을 맡고 싶나요?
    CEO
    당신의 커리어는 어떻게 되나요?
    엔비디아 연구원
    직무와 관련해, 당신의 관심사는 무엇인가요?
    뉴로모픽 반도체
    당신의 업무철학은 어떻게 되나요?
    성장
    """,
    """
    당신의 MBTI는 무엇입니까?
    INFP
    직무와 관련해, 어떤 역할을 맡고 싶나요?
    월급루팡
    당신의 커리어는 어떻게 되나요?
    카이스트 교수
    직무와 관련해, 당신의 관심사는 무엇인가요?
    컴퓨터 비전
    당신의 업무철학은 어떻게 되나요?
    뺨은 안때리는 교수가 될거야!
    """,
    """
    당신의 MBTI는 무엇입니까?
    ESTP
    직무와 관련해, 어떤 역할을 맡고 싶나요?
    회계 관리
    당신의 커리어는 어떻게 되나요?
    삼성 회계관리사
    직무와 관련해, 당신의 관심사는 무엇인가요?
    엔비디아 주식
    당신의 업무철학은 어떻게 되나요?
    주식대박
    """
]

def initialize():
    load_dotenv()

    try:
        client = OpenAI(
            api_key=os.environ.get('UPSTAGE_API_KEY'), base_url="https://api.upstage.ai/v1/solar"
        )
    except Exception as e:
        print("Fail to get upstage api key")
    try:
        con = oracledb.connect(user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD"), dsn=os.environ.get("DSN"))
    except Exception as e:
        print("Connection failed!")

    return client, con

def User_char():

    UserAnswer=""

    Answer1=input("당신의 MBTI는 무엇입니까?\n")
    UserAnswer+="\n당신의 MBTI는 무엇입니까?\n"+Answer1

    Answer2=input("직무와 관련해, 어떤 역할을 맡고 싶나요?\n")
    UserAnswer+="\n직무와 관련해, 어떤 역할을 맡고 싶나요?\n"+Answer2

    Answer3=input("당신의 커리어는 어떻게 되나요?\n")
    UserAnswer+="\n당신의 커리어는 어떻게 되나요?\n"+Answer3

    Answer4=input("직무와 관련해, 당신의 관심사는 무엇인가요?\n")
    UserAnswer+="\n직무와 관련해, 당신의 관심사는 무엇인가요?\n"+Answer4

    Answer5=input("당신의 업무철학은 어떻게 되나요?\n")
    UserAnswer+="당신의 업무철학은 어떻게 되나요?\n"+Answer5

    Char_list.append(UserAnswer)

def chat(vector_store):
    llm = ChatUpstage()
    iinput=input("어떤 사람을 만나고 싶은지 설명해 주실래요?\n")
    retriever = vector_store.as_retriever()
    result_docs = retriever.invoke(iinput)

    for i in range(4):    
        template = """너는 이제 아래의 데이터를 가진 사람이야. 만약에 가지고 있지 않는 너의 데이터에 대해서 물어보면, 너가 무작위로 관련된 정보들을 생성해서 대답해 줘. 예를 들어서, 이름을 물어보면 너의 이름을 무작위로 생성해서 대답해야 해.:"""
        temp = """
                {context} 
                Question: {question} 
                Output: please, response in Korean
                """

    print("\n")
    print("="*50)
    print("말씀하신 특성을 가지고 있는 사람과 연결이 완료되었습니다.\n")
    print("자유롭게 대화하시고, 대화를 종료하고 싶으시다면 \'exit\'을 입력해 주세요.\n")
    print("만약, 다른 사람과의 매칭을 원하신다면 \'again\'을 입력해 주세요.\n")
    print("="*50)
    print("\n")

    print("안녕하세요?\n")

    while(1):
      prompt = PromptTemplate.from_template(template + temp)
      chain = prompt | llm | StrOutputParser()

      uinput = input()
      if "exit" in uinput:
          return 0
      elif "again" in uinput:
          return 1
          

      response = chain.invoke({"question": uinput, "context": [result_docs[i]]})
      #print("Question: ", uinput)
      #print("-"*100)
      print(response)
      print("\n")

      template += "Quesetion: " + uinput
      template += "Answer: " + response 

      #next = input("대화를 종료하시겠습니까? (y/n)\n")
      #if next == "y" :
        #break


if __name__=="__main__":
    client, con = initialize()

    User_char()
    cdocs = [Document(page_content=text) for text in Char_list]

    upstage_embeddings = UpstageEmbeddings(model="solar-embedding-1-large")

    knowledge_base = OracleVS.from_documents(cdocs, upstage_embeddings, client=con, 
                    table_name="text_embeddings2", 
                    distance_strategy=DistanceStrategy.DOT_PRODUCT)   

    vector_store = OracleVS(client=con,
                        embedding_function=upstage_embeddings, 
                        table_name="text_embeddings2", 
                        distance_strategy=DistanceStrategy.DOT_PRODUCT)
    
    if (chat(vector_store)):
        chat(vector_store)