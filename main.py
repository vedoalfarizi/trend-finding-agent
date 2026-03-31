import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from service import AgentService
from pydantic import BaseModel

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")

    app.state.agent_service = AgentService(
        project_id=project_id,
        location=location
    )

    print(f"Agent service initialized for project: {project_id}")

    yield

    print("Shutting down agent service...")

app = FastAPI(lifespan=lifespan)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"Status": "FastAPI is running!"}

@app.post("/ask")
async def ask_agent(request: Request, chat: ChatRequest):
    service: AgentService = request.app.state.agent_service

    response_text = await service.get_response(chat.message)

    return {"status": "success", "agent_response": response_text}