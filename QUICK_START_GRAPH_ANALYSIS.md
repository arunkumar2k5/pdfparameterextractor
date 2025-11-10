# Quick Start: Graph Analysis Feature

## 🚀 Get Started in 3 Steps

### Step 1: Ensure Configuration
Check your `backend/.env` file has:
```bash
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o
```

### Step 2: Start Services

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Step 3: Use the Feature

1. Open http://localhost:3000
2. Click **"Graph Analysis"** tab
3. Click **"Upload Graph (JPG, PNG)"**
4. Select your graph image
5. Click **"Process Graph"**
6. Wait 10-30 seconds for AI analysis
7. Enter **x values** to calculate **y values**

## 📸 What Graphs Work Best?

✅ **Good:**
- Clear axis labels
- High resolution
- Single or multiple distinct curves
- Standard mathematical functions

❌ **Avoid:**
- Blurry or low-quality images
- Handwritten graphs
- Graphs with excessive noise
- 3D plots (not yet supported)

## 🧮 Equation Examples

The AI can extract various equation types:

| Graph Type | Example Equation |
|------------|------------------|
| Linear | `y = 2*x + 3` |
| Quadratic | `y = x^2 - 4*x + 5` |
| Exponential | `y = 2*e^(0.5*x)` |
| Logarithmic | `y = log(x) + 1` |
| Trigonometric | `y = sin(2*pi*x)` |
| Polynomial | `y = x^3 - 2*x^2 + x - 1` |

## 💡 Tips

1. **Better Images = Better Results**
   - Use high-resolution scans or screenshots
   - Ensure good contrast
   - Clear axis labels help accuracy

2. **Multiple Curves**
   - AI automatically detects multiple curves
   - Each gets its own equation and calculator
   - Curves should be visually distinct

3. **X Value Input**
   - Enter any numeric value
   - Y is calculated instantly
   - Works with decimals and negatives

4. **Troubleshooting**
   - If equation fails, check backend logs
   - Try re-uploading with better quality
   - Verify API key is valid

## 🎯 Example Use Case

**Scenario**: You have a datasheet with a temperature vs. resistance graph

1. Screenshot or scan the graph
2. Upload to Graph Analysis tab
3. AI extracts: `y = 1000 * (1 + 0.00385*x)`
4. Enter temperature (x = 25°C)
5. Get resistance (y = 1096.25 Ω)

## 🔧 Testing

Test the analyzer directly:
```bash
cd backend
python test_graph_analyzer.py path/to/your/graph.jpg
```

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| "API key not configured" | Add `OPENAI_API_KEY` to `.env` |
| "Model does not support vision" | Change to `OPENAI_MODEL=gpt-4o` |
| "Invalid equation" | AI returned complex equation - try simpler graph |
| Slow processing | Normal - Vision API takes 10-30 seconds |

## 📊 Cost

- ~$0.01 per graph analysis (GPT-4o pricing)
- Calculations are free (done in browser)

## 🎓 Learn More

- Full documentation: `GRAPH_ANALYSIS_FEATURE.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
- Model selection: `MODEL_GUIDE.md`

## ✅ Quick Checklist

Before using:
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] OpenAI API key configured
- [ ] Model set to `gpt-4o`
- [ ] Graph image ready (JPG/PNG)

Ready to analyze graphs! 🚀
