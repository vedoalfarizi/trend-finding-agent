from agents.cloud_agent import CloudAgent
from agents.sequential_agent import SequentialAgent
from utils.logger import get_logger

logger = get_logger(__name__)


def get_cloud_agent(
    project_id: str, location: str, model_id: str, instruction: str = None
) -> CloudAgent:
    """
    Create and return a CloudAgent instance specialized in Google Cloud Platform.

    Args:
        project_id: GCP project ID.
        location: GCP location.
        model_id: Model ID to use.
        instruction: System instruction for the agent (GCP-focused by default).

    Returns:
        Initialized CloudAgent instance with GCP specialization.
    """
    if instruction is None:
        instruction = (
            "You are a specialized Google Cloud Platform (GCP) assistant. "
            "You have deep knowledge of GCP services, best practices, and solutions. "
            "Only answer questions related to Google Cloud Platform. "
            "If a question is not GCP-related, politely decline and redirect the user to ask GCP-related questions. "
            "Provide clear, concise, and accurate responses."
        )

    logger.info(f"Creating CloudAgent with model {model_id}")
    return CloudAgent(
        name="cloud_assistant",
        instruction=instruction,
        project_id=project_id,
        location=location,
        model_id=model_id,
    )


def get_sequential_agent(
    project_id: str, location: str, model_id: str, instruction: str = None
) -> SequentialAgent:
    """
    Create and return a SequentialAgent instance.

    Args:
        project_id: GCP project ID.
        location: GCP location.
        model_id: Model ID to use.
        instruction: System instruction for the agent.

    Returns:
        Initialized SequentialAgent instance.
    """
    if instruction is None:
        instruction = (
            "You are a sequential processing agent. "
            "Break down complex requests, execute them step by step, and provide comprehensive responses."
        )

    logger.info(f"Creating SequentialAgent with model {model_id}")
    return SequentialAgent(
        name="sequential_assistant",
        instruction=instruction,
        project_id=project_id,
        location=location,
        model_id=model_id,
    )
