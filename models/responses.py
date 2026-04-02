from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """Response model for chat endpoints."""

    status: str = Field(..., description="Status of the request (e.g., 'success' or 'error')")
    agent_response: str = Field(..., description="Response from the agent")
    agent_type: str = Field(
        ..., description="Type of agent used (e.g., 'simple' or 'sequential')"
    )

    class Config:
        """Model configuration."""
        example = {
            "status": "success",
            "agent_response": "This is the agent's response.",
            "agent_type": "simple",
        }


class ErrorResponse(BaseModel):
    """Response model for error cases."""

    status: str = Field(default="error", description="Error status")
    detail: str = Field(..., description="Error detail message")

    class Config:
        """Model configuration."""
        example = {
            "status": "error",
            "detail": "An error occurred while processing your request.",
        }
