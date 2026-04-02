from fastapi import APIRouter, Request, HTTPException

from models.requests import ChatRequest
from models.responses import ChatResponse, ErrorResponse
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/ask", response_model=ChatResponse)
async def ask_simple_agent(request: Request, chat: ChatRequest) -> ChatResponse:
    """
    Chat endpoint using SimpleAgent.

    Process user message with the simple agent and return response.

    Args:
        request: FastAPI request object with app state.
        chat: Chat request containing user message.

    Returns:
        Chat response with status and agent response.

    Raises:
        HTTPException: If an error occurs during processing.
    """
    try:
        logger.info(f"Received request: {chat.message[:50]}...")

        # Get simple agent from app state
        simple_agent = request.app.state.simple_agent

        # Run agent
        response_text = await simple_agent.run(chat.message)

        logger.info("SimpleAgent response generated successfully")
        return ChatResponse(
            status="success",
            agent_response=response_text,
            agent_type="simple",
        )

    except Exception as e:
        logger.error(f"Error in /ask endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}",
        )
