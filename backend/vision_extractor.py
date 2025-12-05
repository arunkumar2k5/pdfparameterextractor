"""
Vision-based analysis using AI models that support image input.
Supports OpenAI GPT-4 Vision and OpenRouter vision models.
"""

import base64
import json
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from config import APIConfig

# Load environment variables
load_dotenv()


class VisionExtractor:
    """Extract information from images using vision-capable AI models"""
    
    def __init__(self, api_key: str = None, provider: str = None):
        """
        Initialize Vision extractor with support for OpenAI and OpenRouter vision models.
        
        Args:
            api_key: API key. If None, reads from config/env
            provider: API provider ('openai' or 'openrouter'). If None, reads from config
        """
        # Determine provider
        self.provider = provider or APIConfig.API_PROVIDER
        
        # Validate configuration
        is_valid, error_msg = APIConfig.validate_config()
        if not is_valid and not api_key:
            raise ValueError(f"Configuration error: {error_msg}")
        
        # Get API key
        self.api_key = api_key or APIConfig.get_api_key()
        if not self.api_key:
            raise ValueError(f"API key not provided for {self.provider}. Set in .env file or pass as parameter.")
        
        # Get base URL and model
        self.base_url = APIConfig.get_base_url()
        self.model = APIConfig.get_vision_model()
        
        # Initialize OpenAI client (works for both OpenAI and OpenRouter)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        print(f"🔍 Initialized Vision Extractor with {self.provider.upper()} - Model: {self.model}")
    
    def analyze_image(self, image_data: bytes, prompt: str, image_format: str = "jpeg") -> Dict[str, Any]:
        """
        Analyze an image with a custom prompt.
        
        Args:
            image_data: Raw image bytes
            prompt: User's question or instruction about the image
            image_format: Image format (jpeg, png, etc.)
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Encode image to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Create the vision message
            system_prompt = self._get_system_prompt()
            print(f"🔍 DEBUG: System prompt: {system_prompt[:100]}...")
            print(f"🔍 DEBUG: User prompt: {prompt[:150]}...")
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{image_format};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            # Make API call (without JSON mode for vision models)
            # Use lower temperature for more focused, deterministic responses
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0,  # Use 0 for most deterministic/focused answers
                max_tokens=APIConfig.MAX_TOKENS
            )
            
            # Extract response
            answer = response.choices[0].message.content
            
            return {
                "success": True,
                "answer": answer,
                "model": self.model,
                "provider": self.provider
            }
            
        except Exception as e:
            print(f"Vision analysis error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "answer": None
            }
    
    def analyze_graph(self, image_data: bytes, question: str) -> Dict[str, Any]:
        """
        Analyze a graph image and answer questions about it.
        
        Args:
            image_data: Raw image bytes of the graph
            question: Question about the graph (e.g., "What is the voltage at 0.6A at 25°C?")
            
        Returns:
            Dictionary with analysis results
        """
        enhanced_prompt = f"""IMPORTANT: Answer ONLY the specific question asked by the user. Do not provide general analysis unless requested.

User's Question: {question}

Instructions:
- Read the graph carefully and locate the exact values requested
- Provide a direct, specific answer to the question
- Include numerical values with proper units
- If you need to interpolate between data points, do so carefully
- Be concise and precise

Answer the question directly:"""

        print(f"🔍 DEBUG: Sending question to AI: {question}")
        print(f"🔍 DEBUG: Using model: {self.model}")
        return self.analyze_image(image_data, enhanced_prompt)
    
    def extract_equation(self, image_data: bytes) -> Dict[str, Any]:
        """
        Extract the mathematical equation from a graph.
        
        Args:
            image_data: Raw image bytes of the graph
            
        Returns:
            Dictionary with equation and analysis
        """
        prompt = """Analyze this graph and provide:

1. The mathematical equation or relationship shown (e.g., y = mx + b, exponential, logarithmic, etc.)
2. Key parameters and their values
3. The type of relationship (linear, exponential, polynomial, etc.)
4. Any important characteristics (slope, intercepts, asymptotes, etc.)

Format your response clearly with the equation prominently displayed."""

        return self.analyze_image(image_data, prompt)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for vision analysis"""
        return """You are a precise technical graph reader specialized in extracting exact values from engineering graphs and charts.

CRITICAL RULES:
1. Answer ONLY what is specifically asked - do not provide extra analysis
2. Read numerical values directly from the graph axes and data points
3. When interpolating, state that you are interpolating
4. Always include units with numerical values
5. Be concise and direct in your answers

Your task is to answer the user's specific question by reading the graph accurately."""
    
    def test_connection(self) -> bool:
        """Test if Vision API connection works"""
        try:
            # Create a simple test with text only
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"Vision API connection test failed: {str(e)}")
            return False


# Test function
if __name__ == "__main__":
    # Test the extractor
    extractor = VisionExtractor()
    
    if extractor.test_connection():
        print("✓ Vision API connection successful!")
    else:
        print("✗ Vision API connection failed!")
