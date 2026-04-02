from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.settings import settings
from routes import chat, sequential
from services.agent_factory import get_cloud_agent, get_sequential_agent
from utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.

    Initializes agents on startup and performs cleanup on shutdown.
    """
    try:
        logger.info("Starting FastAPI application with agents...")

        # Initialize CloudAgent (GCP-specialized)
        app.state.cloud_agent = get_cloud_agent(
            project_id=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION,
            model_id=settings.MODEL_ID,
            instruction="You are a specialized Google Cloud Platform (GCP) assistant with deep knowledge of GCP services. Only answer GCP-related questions.",
        )

        # Initialize SequentialAgent
        app.state.sequential_agent = get_sequential_agent(
            project_id=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION,
            model_id=settings.MODEL_ID,
            instruction=(
                "You are a sequential processing agent. "
                "Break down complex requests, execute them step by step, and provide comprehensive responses."
            ),
        )

        logger.info(
            f"Agents initialized successfully for project: {settings.GOOGLE_CLOUD_PROJECT}"
        )

        yield

        logger.info("Shutting down FastAPI application...")

    except Exception as e:
        logger.error(f"Error during application startup: {str(e)}", exc_info=True)
        raise


# Create FastAPI application with lifespan context manager
app = FastAPI(
    title="Sequential Agent API",
    description="FastAPI application with CloudAgent (GCP-specialized) and SequentialAgent",
    version="1.0.0",
    lifespan=lifespan,
)


# Include routes
app.include_router(chat.router)
app.include_router(sequential.router)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "status": "running",
        "message": "Sequential Agent API is operational",
        "endpoints": {
            "cloud": "/ask",
            "sequential": "/ask-sequential",
            "health": "/docs",
        },
    }
