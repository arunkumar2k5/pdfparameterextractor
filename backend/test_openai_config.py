"""
Test script to verify OpenAI API configuration and extraction
"""
import os
from dotenv import load_dotenv
from openai_extractor import OpenAIExtractor

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if API key is configured"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env file")
        print("   Please add: OPENAI_API_KEY=your-api-key-here")
        return False
    
    # Mask the key for display
    masked_key = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
    print(f"✓ OPENAI_API_KEY found: {masked_key}")
    return True

def test_connection():
    """Test OpenAI connection"""
    try:
        print("\n🔌 Testing OpenAI connection...")
        extractor = OpenAIExtractor()
        
        if extractor.test_connection():
            print("✓ OpenAI connection successful!")
            return True
        else:
            print("❌ OpenAI connection failed")
            return False
    except Exception as e:
        print(f"❌ Connection test error: {str(e)}")
        return False

def test_extraction():
    """Test parameter extraction with sample data"""
    try:
        print("\n🧪 Testing parameter extraction...")
        
        sample_markdown = """
# TPS54360 Buck Converter Datasheet

## Absolute Maximum Ratings
- Input Voltage: -0.3V to 60V
- Junction Temperature: -40°C to 150°C

## Electrical Characteristics
| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| Input Voltage Range | 4.5 | - | 60 | V |
| Output Voltage Range | 0.8 | - | 58 | V |
| Output Current | - | - | 3.5 | A |
| Feedback Voltage | 0.784 | 0.8 | 0.816 | V |
| Junction Temperature | -40 | - | 150 | °C |
"""
        
        parameters = [
            "Input voltage Max",
            "Output voltage Max",
            "Output current Max",
            "Feedback voltage Max",
            "Junction Temperature Max"
        ]
        
        extractor = OpenAIExtractor()
        results = extractor.extract_parameters(sample_markdown, parameters)
        
        print(f"\n📊 Extraction Results ({len(results)} parameters):")
        print("-" * 80)
        
        for r in results:
            status = "✓" if r['value'] != "NF" else "✗"
            print(f"{status} {r['name']}: {r['value']} {r['unit']} (confidence: {r['confidence']}%)")
            if r['source_text']:
                print(f"   Source: {r['source_text'][:100]}...")
        
        found_count = sum(1 for r in results if r['value'] != "NF")
        print("-" * 80)
        print(f"Summary: {found_count}/{len(results)} parameters extracted successfully")
        
        return found_count > 0
        
    except Exception as e:
        print(f"❌ Extraction test error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("OpenAI Configuration Test")
    print("=" * 80)
    
    # Run tests
    api_ok = test_api_key()
    
    if api_ok:
        conn_ok = test_connection()
        
        if conn_ok:
            extract_ok = test_extraction()
            
            print("\n" + "=" * 80)
            if extract_ok:
                print("✅ All tests passed! OpenAI extraction is working correctly.")
            else:
                print("⚠️  Connection works but extraction failed. Check the logs above.")
        else:
            print("\n" + "=" * 80)
            print("❌ Connection test failed. Check your API key and internet connection.")
    else:
        print("\n" + "=" * 80)
        print("❌ API key not configured. Please set OPENAI_API_KEY in backend/.env")
    
    print("=" * 80)
