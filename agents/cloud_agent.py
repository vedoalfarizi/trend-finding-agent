from google import genai
from google.adk.agents import Agent

from google.genai import types

from agents.base_agent import BaseAgent
from utils.logger import get_logger

logger = get_logger(__name__)


class CloudAgent(BaseAgent):
    """Cloud agent specialized in Google Cloud Platform (GCP) queries.
    
    This agent is designed to answer questions specifically related to Google Cloud Platform,
    providing guidance on GCP services, best practices, and solutions.
    """

    def __init__(
        self,
        name: str,
        instruction: str,
        project_id: str,
        location: str,
        model_id: str,
    ):
        """Initialize the cloud agent with GCP specialization."""
        super().__init__(name, instruction, project_id, location, model_id)

        # Initialize Vertex AI client
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
        )

        # Create Agent instance with GCP-focused instructions
        self.agent = Agent(
            name=name,
            instruction=instruction,
        )

        logger.info(f"CloudAgent '{name}' initialized for project {project_id}")

    async def run(self, user_input: str) -> str:
        """
        Process user input and return GCP-related response.

        Uses the system instruction to guide the model's behavior for GCP queries.

        Args:
            user_input: User input/query related to Google Cloud Platform.

        Returns:
            Model response as string with GCP guidance.
        """
        logger.info(f"CloudAgent processing input: {user_input[:50]}...")

        try:
            # Call Vertex AI with system instruction to ensure GCP-focused responses
            
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=self.instruction,
                )
            )
            result = response.text
            logger.info(f"CloudAgent response generated successfully")
            return result

        except Exception as e:
            logger.error(f"CloudAgent error: {str(e)}", exc_info=True)
            raise
