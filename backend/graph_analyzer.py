"""
Graph analyzer using OpenAI Vision API to extract equations from graph images.
"""

import base64
import json
import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GraphAnalyzer:
    """Analyze graph images and extract equations using OpenAI Vision API"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize Graph Analyzer.
        
        Args:
            api_key: OpenAI API key. If None, reads from .env file
            model: OpenAI model name. If None, reads from .env file (defaults to gpt-4o)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY in .env file or pass as parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        # For vision tasks, use gpt-4o or gpt-4-vision-preview
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4o')
        
        # Ensure we're using a vision-capable model
        if 'vision' not in self.model.lower() and 'gpt-4o' not in self.model.lower():
            print(f"⚠️  Model {self.model} may not support vision. Using gpt-4o instead.")
            self.model = 'gpt-4o'
        
        print(f"✓ Graph analyzer initialized with model: {self.model}")
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_graph(self, image_path: str, custom_question: str = None) -> Dict[str, Any]:
        """
        Analyze a graph image and extract equations or answer a custom question.
        
        Args:
            image_path: Path to the graph image file
            custom_question: Optional custom question to ask about the graph
            
        Returns:
            Dictionary containing curves with equations and metadata, or question answer
        """
        try:
            print(f"📊 Analyzing graph: {image_path}")
            if custom_question:
                print(f"❓ Custom question: {custom_question}")
            
            # Encode image
            base64_image = self.encode_image(image_path)
            
            # Create the prompt based on whether there's a custom question
            if custom_question:
                prompt = self._get_question_prompt(custom_question)
            else:
                prompt = self._get_analysis_prompt()
            
            # Call OpenAI Vision API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing technical graphs and extracting mathematical equations from them."
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
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            response_content = response.choices[0].message.content
            print(f"\n📥 Raw OpenAI Response:")
            print("=" * 80)
            print(response_content)
            print("=" * 80)
            
            # If custom question, return answer directly
            if custom_question:
                result = json.loads(response_content)
                answer = result.get('answer', response_content)
                print(f"\n✓ Question answered")
                return {
                    "success": True,
                    "question_answer": answer,
                    "curves": []
                }
            
            # Otherwise, parse equation extraction
            result = json.loads(response_content)
            print(f"\n✓ Analysis complete: Found {len(result.get('curves', []))} curve(s)")
            
            # Log each equation
            for i, curve in enumerate(result.get('curves', []), 1):
                print(f"  Curve {i}: {curve.get('name', 'Unnamed')}")
                print(f"    Equation: {curve.get('equation', 'N/A')}")
            
            return self._format_result(result)
            
        except Exception as e:
            print(f"❌ Graph analysis error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "curves": [],
                "error": str(e)
            }
    
    def _get_analysis_prompt(self) -> str:
        """Get the analysis prompt for the AI"""
        return """Analyze this graph image and extract the following information:

1. **Identify all curves/lines** in the graph
2. **Determine the mathematical equation** for each curve
3. **Identify axis labels** (x-axis and y-axis)
4. **Estimate the range** of x values shown
5. **Provide any additional notes** about the curves

**CRITICAL REQUIREMENT - EQUATION FORMAT:**
- You MUST provide a valid mathematical equation that can be computed
- The equation MUST be in the format: y = [mathematical expression with x]
- DO NOT use descriptive text like "approximately linear" or "slight slope"
- ALWAYS provide actual numbers and mathematical operators

**Valid Examples:**
- Linear: y = 0.05*x + 0.1
- Quadratic: y = 0.01*x^2 + 0.02*x + 0.15
- Exponential: y = 0.2*e^(0.1*x)
- Constant: y = 0.25

**Invalid Examples (DO NOT USE):**
- "Approximately linear, slight positive slope" ❌
- "Increases gradually" ❌
- "Positive correlation" ❌

**Instructions:**
- Use standard mathematical notation: * for multiplication, ^ for power, / for division
- If multiple curves exist, identify each one separately
- Estimate coefficients from the graph (e.g., if line goes from (4, 0.15) to (6, 0.35), calculate slope)
- For linear curves: calculate y = m*x + b where m is slope and b is y-intercept
- If exact equation is complex, provide polynomial approximation
- Include actual numeric values, not descriptions

**Return JSON format:**
{
  "graph_description": "Brief description of what the graph shows",
  "curves": [
    {
      "name": "Curve 1" or descriptive name if labeled,
      "equation": "y = [MUST BE VALID MATH EXPRESSION WITH NUMBERS]",
      "x_axis": "x-axis label",
      "y_axis": "y-axis label",
      "x_range": "approximate x range (e.g., '3.8 to 6')",
      "notes": "any additional observations about this curve"
    }
  ]
}

REMEMBER: The equation field MUST contain a computable mathematical expression, not a description!"""
    
    def _get_question_prompt(self, question: str) -> str:
        """Get the prompt for answering a custom question about the graph"""
        return f"""Analyze this graph image and answer the following question:

**Question:** {question}

**Instructions:**
- Carefully examine the graph to find the relevant information
- Look at axis labels, curve labels, legends, and data points
- Provide a specific, accurate answer based on what you can see in the graph
- If the exact value is not shown, provide the closest approximation
- Include units in your answer if applicable
- If you cannot determine the answer from the graph, explain why

**Return JSON format:**
{{
  "answer": "Your detailed answer to the question, including specific values and units"
}}

Be precise and thorough in your answer."""
    
    def _format_result(self, result: Dict) -> Dict[str, Any]:
        """Format the result to match expected output structure"""
        curves = result.get("curves", [])
        
        # Add IDs to curves
        formatted_curves = []
        for i, curve in enumerate(curves):
            formatted_curve = {
                "id": f"curve-{i+1}",
                "name": curve.get("name", f"Curve {i+1}"),
                "equation": curve.get("equation", ""),
                "x_axis": curve.get("x_axis", "x"),
                "y_axis": curve.get("y_axis", "y"),
                "x_range": curve.get("x_range", ""),
                "notes": curve.get("notes", "")
            }
            formatted_curves.append(formatted_curve)
        
        return {
            "success": True,
            "curves": formatted_curves,
            "graph_description": result.get("graph_description", "")
        }


# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python graph_analyzer.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    try:
        analyzer = GraphAnalyzer()
        result = analyzer.analyze_graph(image_path)
        
        print("\n" + "="*80)
        print("Graph Analysis Result")
        print("="*80)
        
        if result["success"]:
            print(f"\nDescription: {result.get('graph_description', 'N/A')}")
            print(f"\nFound {len(result['curves'])} curve(s):\n")
            
            for curve in result['curves']:
                print(f"📈 {curve['name']}")
                print(f"   Equation: {curve['equation']}")
                print(f"   X-axis: {curve['x_axis']}")
                print(f"   Y-axis: {curve['y_axis']}")
                if curve['x_range']:
                    print(f"   Range: {curve['x_range']}")
                if curve['notes']:
                    print(f"   Notes: {curve['notes']}")
                print()
        else:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
        
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
