from summary_chatbot.prompts.prompt import PROMPT_SUMMARIZE,SYSTEM_PROMPT
import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.graph import MessagesState, END
from typing import Literal


load_dotenv() #needed for the file to see my api key and model type (env variables)

class State(MessagesState): #function to memorise the chat history
    history: str

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
        temperature=0.2,
        openai_api_key=os.environ['OPENAI_API_KEY'],
        model=os.environ['MODEL_ID']
    )
    # If a summary exists, we add this in as a system message
    history = state.get("history", "")
    if history:
        system_message = f"Summary of conversation earlier: {history}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        system_message = SYSTEM_PROMPT.format(conversation=conversation_summary)
        messages = [SystemMessage(content=system_message)] + state["messages"]
    response = llm.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

def summarize_history(state: State) -> dict:
    llm_summarize = ChatOpenAI(
        temperature=0.2,
        openai_api_key=os.environ['OPENAI_API_KEY'],
        model=os.environ['MODEL_ID']
    )
    history = state.get("history", "")
    if history:
        history_message = (f"Summary of conversation earlier: {history}")
    else:
        history_message = "No conversation history available"
    message = state["messages"] + [HumanMessage(content=history_message)]
    response = llm_summarize.invoke(message)
    delete_message = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"history": response.content, "messages": delete_message}

# cleaner version, because end works as a value in the graph, 
# but not as a return type in the function, so we need to use a string instead
def should_continue(state: State) -> Literal["summarize_history", "__end__"]:
    message = state["messages"]
    if len(message) > 6:
        return "summarize_history"
    return END

# obj --> appeller mon modèle, s'il y a un histique conversationel, l'afficher.
# fonction qui affiche le doctionnaire, pour voir ou on en est le chatbot
def print_update(update: dict) -> None:
    for k, v in update.items():
        for m in v["messages"]:
            m.pretty_print()
        if "history" in v:
            print(v["history"])