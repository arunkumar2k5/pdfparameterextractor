"""
AI-powered parameter extraction from markdown datasheets.
Supports both OpenAI and OpenRouter APIs for intelligent parameter extraction.
"""

import json
import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from config import APIConfig

# Load environment variables
load_dotenv()


class OpenAIExtractor:
    """Extract parameters from markdown using AI (OpenAI or OpenRouter)"""
    
<<<<<<< HEAD
    def __init__(self, api_key: str = None, model: str = None):
=======
    def __init__(self, api_key: str = None, provider: str = None):
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
        """
        Initialize AI extractor with support for OpenAI and OpenRouter.
        
        Args:
<<<<<<< HEAD
            api_key: OpenAI API key. If None, reads from .env file
            model: OpenAI model name. If None, reads from .env file (defaults to gpt-3.5-turbo)
=======
            api_key: API key. If None, reads from config/env
            provider: API provider ('openai' or 'openrouter'). If None, reads from config
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
        """
        # Determine provider
        self.provider = provider or APIConfig.API_PROVIDER
        
<<<<<<< HEAD
        self.client = OpenAI(api_key=self.api_key)
        # Read model from parameter, env, or use default
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        print(f"✓ OpenAI extractor initialized with model: {self.model}")
=======
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
        self.model = APIConfig.get_model()
        
        # Initialize OpenAI client (works for both OpenAI and OpenRouter)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        print(f"🤖 Initialized AI Extractor with {self.provider.upper()} - Model: {self.model}")
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
    
    def extract_parameters(self, markdown: str, parameters: List[str], page_mapping: Dict = None) -> List[Dict[str, Any]]:
        """
        Extract parameters from markdown using OpenAI.
        
        Args:
            markdown: Markdown content from PDF
            parameters: List of parameter names to extract
            page_mapping: Optional page mapping for line-to-page conversion
            
        Returns:
            List of extracted parameters with values, units, and metadata
        """
        try:
            prompt = self._build_prompt(markdown, parameters)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
<<<<<<< HEAD
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=4000,  # Increased for more parameters
=======
                temperature=APIConfig.TEMPERATURE,
                max_tokens=APIConfig.MAX_TOKENS,
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            response_content = response.choices[0].message.content
            print(f"📥 Received response from OpenAI ({len(response_content)} chars)")
            result = json.loads(response_content)
            extracted_params = result.get("parameters", [])
            print(f"✓ Extracted {len(extracted_params)} parameters from AI response")
            
            # Post-process to match expected format
            return self._format_results(extracted_params, page_mapping)
            
        except Exception as e:
            print(f"❌ OpenAI extraction error: {str(e)}")
            import traceback
            traceback.print_exc()
            # Return empty results on error
            return [self._create_not_found_result(param) for param in parameters]
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI"""
        return """You are a technical datasheet analyzer specialized in extracting engineering parameters from component datasheets.

Your task is to:
1. Read the markdown-formatted datasheet carefully
2. Find the exact values for requested parameters
3. Extract values with their units
4. Provide confidence scores based on how certain you are
5. Include the source text snippet where you found the value
6. Check for the parameters under the "Electrical Characteristics" section if not found search the rest of the document
7. Look for maximum ratings, absolute maximum ratings, and recommended operating conditions sections
8. For "Max" parameters, look for maximum values in specifications tables

Be precise and only extract values that are explicitly stated in the datasheet.
If a parameter is not found, mark it as "NF" (Not Found)."""
    
    def _build_prompt(self, markdown: str, parameters: List[str]) -> str:
        """Build the extraction prompt"""
        param_list = "\n".join(f"{i+1}. {p}" for i, p in enumerate(parameters))
        
        # Truncate markdown if too long (to stay within token limits)
        # GPT-4 has larger context, so adjust based on model
        if 'gpt-4' in self.model.lower():
            max_chars = 100000  # GPT-4 can handle much more
        else:
            max_chars = 30000  # GPT-3.5 limit
        
        truncated = False
        if len(markdown) > max_chars:
            markdown = markdown[:max_chars] + "\n\n[... datasheet truncated for length ...]"
            truncated = True
            print(f"⚠️  Warning: Markdown truncated to {max_chars} chars")
        
        print(f"📄 Processing {len(parameters)} parameters from {len(markdown)} chars of markdown (truncated: {truncated})")
        
        return f"""Extract the following parameters from this technical datasheet (in markdown format):

**Parameters to find:**
{param_list}

**Datasheet content:**
```markdown
{markdown}
```

**Instructions:**
- Extract exact values from the datasheet
- Include units (V, A, W, °C, µF, etc.)
- For ranges, use format like "1.5 to 6.0" or "10-20"
- If not found, set value to "NF"
- Provide confidence score (0-100) based on certainty
- Include the source text snippet where you found it
- For "Range" parameters, look for min-max values or operating ranges

**Return JSON format:**
{{
  "parameters": [
    {{
      "name": "parameter name",
      "value": "extracted value or NF",
      "unit": "unit symbol",
      "confidence": 95,
      "source_text": "exact text from datasheet",
      "notes": "any additional context"
    }}
  ]
}}"""
    
    def _format_results(self, extracted_params: List[Dict], page_mapping: Dict = None) -> List[Dict[str, Any]]:
        """Format results to match the expected output structure"""
        formatted = []
        
        for param in extracted_params:
            # Determine if found
            value = param.get("value", "NF")
            is_found = value != "NF" and value != ""
            
            result = {
                "name": param.get("name", ""),
                "value": value,
                "unit": param.get("unit", ""),
                "source_page": self._estimate_page(param.get("source_text", ""), page_mapping) if is_found else None,
                "extraction_method": "openai" if is_found else "not_found",
                "confidence": param.get("confidence", 0 if not is_found else 85),
                "manually_edited": False,
                "source_text": param.get("source_text", ""),
                "notes": param.get("notes", ""),
                "markdown_line": None,  # Could be enhanced to find line number
                "highlights": []  # AI mode doesn't provide bounding boxes
            }
            
            formatted.append(result)
        
        return formatted
    
    def _estimate_page(self, source_text: str, page_mapping: Dict = None) -> int:
        """Estimate page number from source text (basic implementation)"""
        # This is a simple estimation - could be improved
        # For now, return page 1 as default
        return 1
    
    def _create_not_found_result(self, param_name: str) -> Dict[str, Any]:
        """Create a not-found result for a parameter"""
        return {
            "name": param_name,
            "value": "NF",
            "unit": "",
            "source_page": None,
            "extraction_method": "not_found",
            "confidence": 0,
            "manually_edited": False,
            "source_text": "",
            "notes": "Not found by OpenAI",
            "markdown_line": None,
            "highlights": []
        }
    
    def test_connection(self) -> bool:
        """Test if OpenAI API connection works"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"OpenAI connection test failed: {str(e)}")
            return False


# Test function
if __name__ == "__main__":
    # Test the extractor
    extractor = OpenAIExtractor()
    
    if extractor.test_connection():
        print("✓ OpenAI connection successful!")
        
        # Test with sample data
        sample_md = """
        # TPS746 Datasheet
        
        ## Specifications
        - Input Voltage Range: 1.5V to 6.0V
        - Output Current: 1A
        - Operating Temperature: -40°C to 125°C
        """
        
        params = ["Input voltage Range", "Output current", "Operating Temperature"]
        results = extractor.extract_parameters(sample_md, params)
        
        print("\nTest extraction results:")
        for r in results:
            print(f"  {r['name']}: {r['value']} {r['unit']} (confidence: {r['confidence']}%)")
    else:
        print("✗ OpenAI connection failed. Check your API key in .env file.")
