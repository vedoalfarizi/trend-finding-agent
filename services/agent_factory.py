from agents.simple_agent import SimpleAgent
from agents.sequential_agent import SequentialAgent
from utils.logger import get_logger

logger = get_logger(__name__)


def get_simple_agent(
    project_id: str, location: str, model_id: str, instruction: str = None
) -> SimpleAgent:
    """
    Create and return a SimpleAgent instance.

    Args:
        project_id: GCP project ID.
        location: GCP location.
        model_id: Model ID to use.
        instruction: System instruction for the agent.

    Returns:
        Initialized SimpleAgent instance.
    """
    if instruction is None:
        instruction = (
            "You are a helpful assistant. Provide clear, concise, and accurate responses."
        )

    logger.info(f"Creating SimpleAgent with model {model_id}")
    return SimpleAgent(
        name="simple_assistant",
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
