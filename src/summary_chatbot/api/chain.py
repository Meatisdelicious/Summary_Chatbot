from summary_chatbot.prompts.prompt import PROMPT_SUMMARIZE

import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage

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

def call_model(state: State, conversation_summary: str) -> dict:
    """
    Calls the language model to generate a response based on the current state and conversation summary.
    Args:
        state (State): The current state of the conversation, including history and messages.
        conversation_summary (str): A summary of the conversation so far.
    Returns:
        dict: A dictionary containing the generated response message.
    """
    llm = ChatOpenAI(
        temperature=os.environ['TEMPERATURE'],
        openai_api_key=os.environ['OPENAI_API_KEY'],
        model=os.environ['OPENAI_MODEL']
    )
    # If a summary exists, we add this in as a system message
    history = state.get("history", "")
    if history:
        system_message = f"Summary of conversation earlier: {history}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        system_message = prompts.SYSTEM_PROMPT.format(conversation=conversation_summary)
        messages = [SystemMessage(content=system_message)] + state["messages"]
    response = llm.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}