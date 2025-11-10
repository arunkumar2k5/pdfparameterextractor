# Graph Analysis Feature

## Overview

The Graph Analysis feature allows you to upload graph images and automatically extract mathematical equations using OpenAI's Vision API. The system can identify multiple curves, determine their equations, and provide an interactive calculator to compute y values for any x input.

## Features

✅ **Image Upload** - Support for JPG, PNG, and other image formats
✅ **AI-Powered Analysis** - Uses OpenAI Vision API (GPT-4o) to understand graphs
✅ **Multi-Curve Detection** - Automatically identifies and extracts equations for multiple curves
✅ **Dynamic Equation Evaluation** - Real-time calculation of y values using math.js
✅ **Interactive Calculator** - Input x values and instantly see computed y results
✅ **Axis Label Detection** - Identifies x-axis and y-axis labels
✅ **Range Estimation** - Provides approximate x-value ranges

## How It Works

### 1. Upload Graph Image
- Click "Upload Graph (JPG, PNG)" button
- Select your graph image file
- Image will be displayed in the left panel

### 2. Process Graph
- Click "Process Graph" button
- OpenAI Vision API analyzes the image
- Extracts equations, axis labels, and curve information

### 3. View Results
- Each detected curve is displayed with:
  - Curve name/label
  - Mathematical equation (in x and y format)
  - X-axis and Y-axis labels
  - Approximate x-value range
  - Additional notes

### 4. Calculate Y Values
- For each curve, enter an x value in the input box
- The y value is automatically calculated and displayed
- Supports any mathematical expression returned by AI

## Technical Implementation

### Frontend (React + TypeScript)
- **Component**: `GraphAnalysis.tsx`
- **Math Library**: `mathjs` for equation evaluation
- **Features**:
  - Image preview
  - Real-time y-value calculation
  - Error handling for invalid equations
  - Responsive design

### Backend (Python + FastAPI)
- **Module**: `graph_analyzer.py`
- **API Endpoint**: `POST /api/analyze-graph`
- **AI Model**: GPT-4o (vision-capable)
- **Features**:
  - Base64 image encoding
  - Structured JSON response
  - Error handling and logging

## Equation Format

The AI returns equations in standard mathematical notation:

```
y = 2*x + 3           (Linear)
y = x^2 + 5*x - 2     (Quadratic)
y = sin(x)            (Trigonometric)
y = e^(-x)            (Exponential)
y = log(x)            (Logarithmic)
```

### Supported Operations
- **Arithmetic**: `+`, `-`, `*`, `/`
- **Power**: `^` (e.g., `x^2`)
- **Trigonometry**: `sin()`, `cos()`, `tan()`
- **Exponential**: `e^x`, `exp()`
- **Logarithm**: `log()`, `ln()`
- **Constants**: `pi`, `e`

## Usage Example

### Input Graph
Upload a graph showing voltage vs. current curves

### AI Output
```json
{
  "graph_description": "Current vs Voltage characteristics for a diode",
  "curves": [
    {
      "name": "Forward Bias",
      "equation": "y = 0.001 * (e^(40*x) - 1)",
      "x_axis": "Voltage (V)",
      "y_axis": "Current (A)",
      "x_range": "0 to 1",
      "notes": "Exponential relationship typical of diode forward bias"
    }
  ]
}
```

### Interactive Calculation
- **Input**: x = 0.7
- **Output**: y = 1.0627 A

## Configuration

### Required Environment Variables
```bash
# .env file
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o  # Vision-capable model required
```

### Supported Models
- ✅ `gpt-4o` (Recommended - fastest and most cost-effective)
- ✅ `gpt-4-vision-preview` (Alternative vision model)
- ❌ `gpt-3.5-turbo` (Does not support vision)

## API Reference

### POST /api/analyze-graph

**Request:**
- Content-Type: `multipart/form-data`
- Body: Image file

**Response:**
```json
{
  "success": true,
  "curves": [
    {
      "id": "curve-1",
      "name": "Curve 1",
      "equation": "y = 2*x + 3",
      "x_axis": "x",
      "y_axis": "y",
      "x_range": "0 to 10",
      "notes": "Linear relationship"
    }
  ],
  "graph_description": "Description of the graph"
}
```

**Error Response:**
```json
{
  "success": false,
  "curves": [],
  "error": "Error message"
}
```

## Troubleshooting

### Issue: "OpenAI API key not configured"
**Solution**: Add `OPENAI_API_KEY` to your `.env` file

### Issue: "Model does not support vision"
**Solution**: Change `OPENAI_MODEL` to `gpt-4o` in `.env` file

### Issue: "Invalid equation" or "Error calculating y"
**Possible Causes**:
- AI returned a complex equation that math.js cannot parse
- Equation contains unsupported functions
- Division by zero or invalid mathematical operation

**Solution**: Check the equation format and try simplifying the graph

### Issue: Inaccurate equations
**Possible Causes**:
- Low-quality or blurry image
- Complex curves that are hard to approximate
- Multiple overlapping curves

**Solution**:
- Use high-resolution images
- Ensure clear axis labels
- Separate complex graphs into simpler ones

## Limitations

1. **Approximation**: AI provides best-fit equations, not exact mathematical derivations
2. **Complex Curves**: Very complex or irregular curves may be difficult to express as simple equations
3. **Image Quality**: Poor quality images may result in inaccurate analysis
4. **Cost**: Each analysis uses OpenAI API credits (GPT-4o vision calls)

## Future Enhancements

- [ ] Support for parametric equations
- [ ] Data point extraction from graphs
- [ ] Curve fitting with user-specified function types
- [ ] Export equations to various formats (LaTeX, Python, etc.)
- [ ] Batch processing of multiple graphs
- [ ] Integration with parameter extraction workflow

## Testing

Test the graph analyzer from command line:

```bash
cd backend
python graph_analyzer.py path/to/your/graph.jpg
```

This will analyze the graph and display extracted equations.

## Dependencies

### Frontend
- `mathjs`: ^12.0.0 - Mathematical expression evaluator
- `lucide-react`: Icons
- `react`: ^18.2.0

### Backend
- `openai`: ^1.0.0 - OpenAI API client
- `python-dotenv`: Environment variable management
- `fastapi`: Web framework
- `python-multipart`: File upload support

## License

Part of the Engineering Parameter Extraction Tool project.
