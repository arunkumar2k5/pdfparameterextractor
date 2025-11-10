"""
Test script for graph analyzer functionality
"""

from graph_analyzer import GraphAnalyzer
import os

def test_graph_analyzer():
    """Test the graph analyzer with a sample or user-provided image"""
    
    print("=" * 80)
    print("Graph Analyzer Test")
    print("=" * 80)
    
    # Check if API key is configured
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n❌ OPENAI_API_KEY not found in environment")
        print("   Please set it in your .env file")
        return False
    
    print(f"\n✓ API key found: {api_key[:7]}...{api_key[-4:]}")
    
    # Initialize analyzer
    try:
        analyzer = GraphAnalyzer()
        print(f"✓ Analyzer initialized with model: {analyzer.model}")
    except Exception as e:
        print(f"\n❌ Failed to initialize analyzer: {str(e)}")
        return False
    
    # Test with a sample image (if provided)
    print("\n" + "-" * 80)
    print("To test with your own graph:")
    print("  python test_graph_analyzer.py path/to/your/graph.jpg")
    print("-" * 80)
    
    # Check if image path provided as argument
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        if not os.path.exists(image_path):
            print(f"\n❌ Image file not found: {image_path}")
            return False
        
        print(f"\n📊 Analyzing graph: {image_path}")
        print("   This may take 10-30 seconds...\n")
        
        result = analyzer.analyze_graph(image_path)
        
        if result["success"]:
            print("\n✅ Analysis Successful!")
            print("=" * 80)
            
            if result.get("graph_description"):
                print(f"\n📝 Description: {result['graph_description']}")
            
            print(f"\n📈 Found {len(result['curves'])} curve(s):\n")
            
            for i, curve in enumerate(result['curves'], 1):
                print(f"{i}. {curve['name']}")
                print(f"   Equation: {curve['equation']}")
                print(f"   X-axis: {curve['x_axis']}")
                print(f"   Y-axis: {curve['y_axis']}")
                if curve.get('x_range'):
                    print(f"   Range: {curve['x_range']}")
                if curve.get('notes'):
                    print(f"   Notes: {curve['notes']}")
                print()
            
            # Test equation evaluation
            print("-" * 80)
            print("Testing Equation Evaluation:")
            print("-" * 80)
            
            from mathjs import evaluate
            
            for curve in result['curves']:
                equation = curve['equation'].replace('y = ', '').replace('y=', '').strip()
                print(f"\n{curve['name']}: {curve['equation']}")
                
                # Test with a few x values
                test_x_values = [0, 1, 5, 10]
                for x in test_x_values:
                    try:
                        y = evaluate(equation, {'x': x})
                        print(f"   x = {x:5} → y = {y:.4f}")
                    except Exception as e:
                        print(f"   x = {x:5} → Error: {str(e)}")
            
            print("\n" + "=" * 80)
            return True
        else:
            print(f"\n❌ Analysis Failed: {result.get('error', 'Unknown error')}")
            return False
    else:
        print("\n✓ Graph analyzer is ready to use!")
        print("   Provide an image path to test analysis.")
        return True

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    success = test_graph_analyzer()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Tests failed. Check the errors above.")
