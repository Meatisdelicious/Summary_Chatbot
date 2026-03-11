from fastapi import FastAPI, UploadFile, File
from summary_chatbot.api.chain import summarise

app = FastAPI()

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