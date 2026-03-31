import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def test_connection():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")

    print(f"Testing connection with project: {project_id} and location: {location}")

    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Hello Vertex AI! Are you working?"
        )
        print(f"connection test successful, received response: {response.text}")
    except Exception as e:
        print(f"Connection test failed with error: {e}")

if __name__ == "__main__":
    test_connection()