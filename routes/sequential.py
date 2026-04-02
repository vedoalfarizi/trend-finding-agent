from fastapi import APIRouter, Request, HTTPException

from models.requests import ChatRequest
from models.responses import ChatResponse, ErrorResponse
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/ask-sequential", response_model=ChatResponse)
async def ask_sequential_agent(request: Request, chat: ChatRequest) -> ChatResponse:
    """
    Chat endpoint using SequentialAgent.

    Process user message with the sequential agent (multi-step processing).

    Args:
        request: FastAPI request object with app state.
        chat: Chat request containing user message.

    Returns:
        Chat response with status and agent response.

    Raises:
        HTTPException: If an error occurs during processing.
    """
    try:
        logger.info(f"Received sequential request: {chat.message[:50]}...")

        # Get sequential agent from app state
        sequential_agent = request.app.state.sequential_agent

        # Run agent
        response_text = await sequential_agent.run(chat.message)

        logger.info("SequentialAgent response generated successfully")
        return ChatResponse(
            status="success",
            agent_response=response_text,
            agent_type="sequential",
        )

    except Exception as e:
        logger.error(f"Error in /ask-sequential endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}",
        )
