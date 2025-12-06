"""
Configuration management for API providers (OpenAI and OpenRouter).
"""

import os
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class APIConfig:
    """Configuration for AI API providers"""
    
    # API Provider Selection
    API_PROVIDER: Literal["openai", "openrouter"] = os.getenv("API_PROVIDER", "openai").lower()
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_VISION_MODEL: str = os.getenv("OPENAI_VISION_MODEL", "gpt-4-vision-preview")
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
    OPENROUTER_VISION_MODEL: str = os.getenv("OPENROUTER_VISION_MODEL", "01-ai/yi-vision")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # Common Configuration
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get the API key based on selected provider"""
        if cls.API_PROVIDER == "openai":
            return cls.OPENAI_API_KEY
        elif cls.API_PROVIDER == "openrouter":
            return cls.OPENROUTER_API_KEY
        else:
            raise ValueError(f"Invalid API provider: {cls.API_PROVIDER}")
    
    @classmethod
    def get_base_url(cls) -> str:
        """Get the base URL based on selected provider"""
        if cls.API_PROVIDER == "openai":
            return cls.OPENAI_BASE_URL
        elif cls.API_PROVIDER == "openrouter":
            return cls.OPENROUTER_BASE_URL
        else:
            raise ValueError(f"Invalid API provider: {cls.API_PROVIDER}")
    
    @classmethod
    def get_model(cls) -> str:
        """Get the model name based on selected provider"""
        if cls.API_PROVIDER == "openai":
            return cls.OPENAI_MODEL
        elif cls.API_PROVIDER == "openrouter":
            return cls.OPENROUTER_MODEL
        else:
            raise ValueError(f"Invalid API provider: {cls.API_PROVIDER}")
    
    @classmethod
    def get_vision_model(cls) -> str:
        """Get the vision model name based on selected provider"""
        if cls.API_PROVIDER == "openai":
            return cls.OPENAI_VISION_MODEL
        elif cls.API_PROVIDER == "openrouter":
            return cls.OPENROUTER_VISION_MODEL
        else:
            raise ValueError(f"Invalid API provider: {cls.API_PROVIDER}")
    
    @classmethod
    def validate_config(cls) -> tuple[bool, str]:
        """
        Validate the configuration.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if cls.API_PROVIDER not in ["openai", "openrouter"]:
            return False, f"Invalid API_PROVIDER: {cls.API_PROVIDER}. Must be 'openai' or 'openrouter'"
        
        api_key = cls.get_api_key()
        if not api_key:
            provider_name = "OPENAI_API_KEY" if cls.API_PROVIDER == "openai" else "OPENROUTER_API_KEY"
            return False, f"{provider_name} not set in .env file"
        
        return True, ""
    
    @classmethod
    def get_provider_info(cls) -> dict:
        """Get information about the current provider configuration"""
        return {
            "provider": cls.API_PROVIDER,
            "model": cls.get_model(),
            "vision_model": cls.get_vision_model(),
            "base_url": cls.get_base_url(),
            "temperature": cls.TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS,
            "has_api_key": bool(cls.get_api_key())
        }


# Create a singleton instance
config = APIConfig()
