from google.adk.agents import Agent

my_agent = Agent(
    name="Assistant",
    instruction="You are a helpful assistant and consice assistant."
)

@my_agent.on_message
def chat(message: str):
    return f"Agent processed: {message}"