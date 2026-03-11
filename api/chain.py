from langchain_openai import ChatOpenAI
import os 
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from prompt import PROMPT_SUMMARIZE # to import the function from the file 

load_dotenv() #needed for the file to see my api key and model type (env variables)

def summarise(conversation : str) -> str:
    prompt_template = PROMPT_SUMMARIZE
    prompt = PromptTemplate(template=prompt_template,input_variables=['text'])
    llm = ChatOpenAI(
        openai_api_key=os.environ['OPENAI_API_KEY'],
        model=os.environ['MODEL_ID'],
        temperature=0.2
    )   
    chain = prompt | llm | StrOutputParser()
    return chain.invoke(conversation)