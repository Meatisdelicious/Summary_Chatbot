from fastapi import FastAPI, UploadFile, File
from summary_chatbot.api.chain import summarise
from summary_chatbot.api.chain import State, call_model, summarize_history, should_continue, print_update, summarise
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from fastapi.responses import StreamingResponse
from fastapi import Body


app = FastAPI()

chain = None

@app.get("/")
async def root():
    print("Hello World")

@app.post("/summarise")
async def summarise_text(file : UploadFile = File(...)):
    if file.content_type != "text/plain":
        return {"error":"only text files are supported"}
    content = await file.read()
    text = content.decode("utf-8")
    summary = summarise(text)
    return {"summary": summary}

@app.post("/initialize")
async def initialize(file: UploadFile = File(...)):
    global chain
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    content = await file.read()
    text = content.decode("utf-8")
    summary = summarise(text)

    # Define a new graph
    workflow = StateGraph(State)
    workflow.add_node("conversation", lambda input: call_model(state=input, conversation_summary=summary))
    workflow.add_node(summarize_history)
    workflow.add_edge(START, "conversation")
    workflow.add_conditional_edges(
        "conversation",
        should_continue,
    )
    workflow.add_edge("summarize_history", END)
    memory = MemorySaver()
    chain = workflow.compile(checkpointer=memory)
    return {"summarise": summary}

async def generate_stream(input_message, config, chain):
    for event in chain.stream({"messages": [input_message]},config=config, stream_mode="updates"):
        yield event["conversation"]["messages"][0].content

@app.post("/update")
async def update(request: str = Body(..., media_type="text/plain")):
    config = {"configurable": {"thread_id": "4"}}
    input_message = HumanMessage(content=request)
    return StreamingResponse(generate_stream(input_message, config, chain), media_type="text/plain")