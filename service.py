from google import genai
from google.adk.agents import Agent

class AgentService:
    def __init__(self, project_id: str, location: str):
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location
        )
        self.model_id = "gemini-2.5-flash"
        self.agent = Agent(
            name="cloud_assistant",
            instruction="You are a helpful assistant and concise assistant that specialized in Google Cloud"
        )

    async def get_response(self, user_input: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=user_input
        )
        return response.text