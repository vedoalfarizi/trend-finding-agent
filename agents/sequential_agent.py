from google import genai

from agents.base_agent import BaseAgent
from utils.logger import get_logger

logger = get_logger(__name__)


class SequentialAgent(BaseAgent):
    """
    Sequential agent that processes requests through multiple steps.

    This agent breaks down a user request into steps:
    1. Planning Step: Analyze the request and plan the approach
    2. Execution Step: Execute the planned steps
    3. Aggregation Step: Combine results and provide final response
    """

    def __init__(
        self,
        name: str,
        instruction: str,
        project_id: str,
        location: str,
        model_id: str,
    ):
        """Initialize the sequential agent."""
        super().__init__(name, instruction, project_id, location, model_id)

        # Initialize Vertex AI client
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
        )

        logger.info(f"SequentialAgent '{name}' initialized for project {project_id}")

    async def run(self, user_input: str) -> str:
        """
        Process user input through sequential steps.

        Steps:
        1. Planning: Break down the request
        2. Execution: Process each step
        3. Aggregation: Combine results

        Args:
            user_input: User input/query.

        Returns:
            Final aggregated response as string.
        """
        logger.info(f"SequentialAgent starting multi-step processing for: {user_input[:50]}...")

        try:
            # ============================================================================
            # STEP 1: PLANNING
            # ============================================================================
            # TODO: Add your planning logic here.
            # This step should break down the user request into sub-tasks.
            # Example: "Given this request, what are the steps needed to solve it?"
            # You can customize:
            # - The prompt used in planning
            # - How to parse the response into discrete steps
            # - Whether to store intermediate results
            # ============================================================================

            planning_prompt = (
                f"Analyze this request and break it down into logical steps:\n\n{user_input}\n\n"
                "Provide a structured plan with numbered steps."
            )

            logger.info("SequentialAgent: Step 1 - Planning phase")
            planning_response = await self._call_model(planning_prompt)
            logger.info(f"Planning output: {planning_response[:100]}...")

            # ============================================================================
            # STEP 2: EXECUTION
            # ============================================================================
            # TODO: Add your execution logic here.
            # This step should execute the plan from Step 1.
            # Example: "Execute the first step from the plan", then "Execute step 2", etc.
            # You can customize:
            # - How many execution iterations to run
            # - Conditional branching based on prior results
            # - Error handling if a step fails
            # - Tool/function calls if needed (simulated here with more model calls)
            # ============================================================================

            execution_prompt = (
                f"Based on this plan:\n{planning_response}\n\n"
                f"And the original request:\n{user_input}\n\n"
                "Execute the plan step by step and provide detailed results for each step."
            )

            logger.info("SequentialAgent: Step 2 - Execution phase")
            execution_response = await self._call_model(execution_prompt)
            logger.info(f"Execution output: {execution_response[:100]}...")

            # ============================================================================
            # STEP 3: AGGREGATION
            # ============================================================================
            # TODO: Add your aggregation logic here.
            # This step should combine results from planning and execution into final response.
            # Example: "Summarize the results", "Extract key insights", "Generate final answer"
            # You can customize:
            # - How to format the final response
            # - Which results to include/exclude
            # - Additional processing or validation
            # - Final quality checks
            # ============================================================================

            aggregation_prompt = (
                f"Original request:\n{user_input}\n\n"
                f"Plan:\n{planning_response}\n\n"
                f"Execution results:\n{execution_response}\n\n"
                "Provide a concise, comprehensive final response that addresses the original request. "
                "Synthesize all the above information into a clear, actionable answer."
            )

            logger.info("SequentialAgent: Step 3 - Aggregation phase")
            final_response = await self._call_model(aggregation_prompt)
            logger.info("SequentialAgent: Multi-step processing completed successfully")

            return final_response

        except Exception as e:
            logger.error(f"SequentialAgent error: {str(e)}", exc_info=True)
            raise

    async def _call_model(self, prompt: str) -> str:
        """
        Helper method to call the Vertex AI model with a prompt.

        Args:
            prompt: The prompt to send to the model.

        Returns:
            Model response as string.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    genai.types.Content(
                        role="user",
                        parts=[genai.types.Part(text=prompt)],
                    )
                ],
                system_instruction=self.instruction,
            )
            return response.text
        except Exception as e:
            logger.error(f"Error calling model: {str(e)}", exc_info=True)
            raise
