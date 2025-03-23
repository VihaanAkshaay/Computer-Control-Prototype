from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from computer_control_project.computer_tools import TypeTool
import uvicorn
from computer_control_project import prog

app = FastAPI(title="Computer Control API")

class TypeTextRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    query: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Computer Control API"}

@app.post("/type_text")
async def type_text(request: TypeTextRequest):
    try:
        tool = TypeTool()
        result = tool._run(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_message(request: ChatRequest):
    try:
        responses = prog.process_user_input(request.query)
        return {"responses": responses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset_chat")
async def reset_chat():
    try:
        prog.reset_chat()
        return {"message": "Chat reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/look_at_chat_history")
async def look_at_chat_history():
    try:
        return prog.look_at_chat_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    # Remove reload=True for production packaging
    uvicorn.run("myserver.main:app", host="0.0.0.0", port=8000)
