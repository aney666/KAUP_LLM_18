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
    llm = ChatUpstage()

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "너는 이제 human으로부터 질문을 하고 답변을 받을 거야."),
            ("system", "첫번째로 human이 말하는 말은 무조건 무시하고 5가지의 질문을 먼저 차례대로 할거야. "),
            ("system", "첫번째 질문은 \"당신의 MBTI는 무엇입니까?\"이야."),
            ("system", "두번째 질문은 \"직무와 관련해, 어떤 역할을 맡고 싶나요?\"이야."),
            ("system", "세번째 질문은 \"당신의 커리어는 어떻게 되나요?\"이야."),
            ("system", "네번째 질문은 \"직무와 관련해, 당신의 관심사는 무엇인가요?\"이야."),
            ("system", "다섯번째 질문은 \"당신의 업무철학은 어떻게 되나요?\"이야."),
            ("system", "질문을 모두 한 후에는 추가로 human에게 더 하고 싶은 말이 있다면 받을 거야."),

            ("human", "I know of it. It's Paris!!"),
            ("ai", "당신의 MBTI는 무엇입니까?"),
            ("human", "ISTP"),
            ("ai", "직무와 관련해, 어떤 역할을 맡고 싶나요?"),
            ("human", "개발자"),
            ("ai", "당신의 커리어는 어떻게 되나요?"),
            ("human", "I know of it. It's Paris!!"),
            ("ai", "직무와 관련해, 당신의 관심사는 무엇인가요?"),
            ("human", "LLM"),
            ("ai", "당신의 업무철학은 어떻게 되나요?"),
            ("human", "돈"),
            ("ai", "더 하고 싶은 말이 있으면 말해주세요."),
            ("human", "없음"),
            ]
        )
    
    chain = chat_prompt | llm | StrOutputParser() # chat_prompt 를 llm으로 리다이렉션 -> String으로 출력하도록 파서에 리다이렉션. 그래서 langchain임
    chain.invoke({})



if __name__=="__main__":
    client = initialize()
    # chat_result = client.chat.completions.create(
    #     model="solar-1-mini-chat",
    #     messages=[
    #         {"role": "system", "content": "Can you tell me good place to vision in Busan?"},
    #     ],
    # )

    # pprint(chat_result.choices[0].message.content)

    first_qna()
