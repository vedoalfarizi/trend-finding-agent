from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoints."""

    message: str = Field(
        ..., min_length=1, max_length=5000, description="User message to send to the agent"
    )

    class Config:
        """Model configuration."""
        example = {"message": "Hello, how can you help me?"}
