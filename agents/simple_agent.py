from google import genai
from google.adk.agents import Agent

from agents.base_agent import BaseAgent
from utils.logger import get_logger

logger = get_logger(__name__)


class SimpleAgent(BaseAgent):
    """Simple agent that responds to user input with system instructions."""

    def __init__(
        self,
        name: str,
        instruction: str,
        project_id: str,
        location: str,
        model_id: str,
    ):
        """Initialize the simple agent."""
        super().__init__(name, instruction, project_id, location, model_id)

        # Initialize Vertex AI client
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
        )

        # Create Agent instance with instructions
        # This agent will use the system instruction in API calls
        self.agent = Agent(
            name=name,
            instruction=instruction,
        )

        logger.info(f"SimpleAgent '{name}' initialized for project {project_id}")

    async def run(self, user_input: str) -> str:
        """
        Process user input and return response.

        Uses the system instruction to guide the model's behavior.

        Args:
            user_input: User input/query.

        Returns:
            Model response as string.
        """
        logger.info(f"SimpleAgent processing input: {user_input[:50]}...")

        try:
            # Call Vertex AI with system_instruction to ensure agent instruction is used
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    genai.types.Content(
                        role="user",
                        parts=[genai.types.Part(text=user_input)],
                    )
                ],
                system_instruction=self.instruction,
            )
            result = response.text
            logger.info(f"SimpleAgent response generated successfully")
            return result

        except Exception as e:
            logger.error(f"SimpleAgent error: {str(e)}", exc_info=True)
            raise
