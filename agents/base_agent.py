from abc import ABC, abstractmethod
from typing import Optional


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(
        self,
        name: str,
        instruction: str,
        project_id: str,
        location: str,
        model_id: str,
    ):
        """
        Initialize the base agent.

        Args:
            name: Name of the agent.
            instruction: System instruction/prompt for the agent.
            project_id: GCP project ID.
            location: GCP location (e.g., 'us-central1').
            model_id: Model ID to use (e.g., 'gemini-2.5-flash').
        """
        self.name = name
        self.instruction = instruction
        self.project_id = project_id
        self.location = location
        self.model_id = model_id

    @abstractmethod
    async def run(self, user_input: str) -> str:
        """
        Execute the agent logic.

        Args:
            user_input: User input or request.

        Returns:
            Agent response as string.
        """
        pass
