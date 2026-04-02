import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Centralized settings for FastAPI app and agent configuration."""

    # GCP Configuration
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    # Model Configuration
    MODEL_ID: str = "gemini-2.5-flash"

    def __post_init__(self):
        """Validate configuration on initialization."""
        if not self.GOOGLE_CLOUD_PROJECT:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT environment variable is not set. "
                "Please configure it in your .env file."
            )
        if not self.GOOGLE_CLOUD_LOCATION:
            raise ValueError(
                "GOOGLE_CLOUD_LOCATION environment variable is not set. "
                "Please configure it in your .env file (e.g., 'us-central1')."
            )

    def to_dict(self) -> dict:
        """Export settings as dictionary for passing to services."""
        return {
            "project_id": self.GOOGLE_CLOUD_PROJECT,
            "location": self.GOOGLE_CLOUD_LOCATION,
            "model_id": self.MODEL_ID,
        }


# Create a singleton settings instance with validation
try:
    settings = Settings()
except ValueError as e:
    raise RuntimeError(f"Configuration Error: {e}") from e
