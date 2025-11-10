# Custom Question Feature for Graph Analysis

## ✅ Feature Added

You can now ask custom questions about graphs instead of just extracting equations!

## 🎯 How It Works

### Two Modes:

1. **Equation Extraction Mode** (default)
   - Leave question field blank
   - AI extracts mathematical equations from curves
   
2. **Question Answering Mode** (new!)
   - Enter a specific question
   - AI analyzes the graph and answers your question

## 📝 Example Questions

```
"What is the dropout voltage at 25°C at 0.6A current?"
"What is the maximum output voltage shown in the graph?"
"At what input voltage does the efficiency drop below 90%?"
"What is the current limit at -40°C?"
"What is the value at x=5?"
```

## 🎨 UI Changes

### New Input Field
Located below the "Process Graph" button:
- Text input for custom questions
- Placeholder with example question
- Helper text explaining the feature

### Answer Display
When a question is asked:
- Shows the question in green header
- Displays AI's answer in white box
- Button to ask another question or switch back to equation mode

## 🔧 Technical Implementation

### Frontend (`GraphAnalysis.tsx`)

**New State:**
```typescript
const [customQuestion, setCustomQuestion] = useState<string>('');
const [questionAnswer, setQuestionAnswer] = useState<string>('');
```

**Question Input:**
```tsx
<input
  type="text"
  value={customQuestion}
  onChange={(e) => setCustomQuestion(e.target.value)}
  placeholder='e.g., "What is the dropout voltage at 25°C at 0.6A current?"'
/>
```

**Answer Display:**
```tsx
{questionAnswer ? (
  <div className="bg-green-50 border border-green-200 rounded-lg p-6">
    <h4>Question: {customQuestion}</h4>
    <div className="bg-white p-4 rounded-lg">
      <p>{questionAnswer}</p>
    </div>
  </div>
) : (
  // Show equations
)}
```

### Backend (`graph_analyzer.py`)

**Updated Method Signature:**
```python
def analyze_graph(self, image_path: str, custom_question: str = None) -> Dict[str, Any]:
```

**New Prompt Method:**
```python
def _get_question_prompt(self, question: str) -> str:
    return f"""Analyze this graph image and answer the following question:
    
**Question:** {question}

**Instructions:**
- Carefully examine the graph to find the relevant information
- Look at axis labels, curve labels, legends, and data points
- Provide a specific, accurate answer based on what you can see
- Include units in your answer if applicable

**Return JSON format:**
{{
  "answer": "Your detailed answer to the question"
}}
"""
```

**Response Handling:**
```python
if custom_question:
    result = json.loads(response_content)
    answer = result.get('answer', response_content)
    return {
        "success": True,
        "question_answer": answer,
        "curves": []
    }
```

### API Endpoint (`main.py`)

**Updated Endpoint:**
```python
@app.post("/api/analyze-graph")
async def analyze_graph(
    file: UploadFile = File(...),
    question: str = None  # New parameter
):
```

## 📊 Response Format

### With Question:
```json
{
  "success": true,
  "question_answer": "The dropout voltage at 25°C at 0.6A current is approximately 0.25V based on the curve labeled '25°C'.",
  "curves": []
}
```

### Without Question (Equation Mode):
```json
{
  "success": true,
  "curves": [
    {
      "id": "curve-1",
      "name": "Curve for -50°C",
      "equation": "y = 0.05*x + 0.1",
      ...
    }
  ],
  "graph_description": "..."
}
```

## 🚀 Usage

### 1. Ask a Question

1. Upload graph image
2. Enter question in text field:
   ```
   What is the dropout voltage at 25°C at 0.6A current?
   ```
3. Click "Process Graph"
4. See answer displayed

### 2. Extract Equations

1. Upload graph image
2. Leave question field **blank**
3. Click "Process Graph"
4. See equations extracted

### 3. Switch Modes

- After getting an answer, click "Ask another question or extract equations"
- Clear the question field to go back to equation mode
- Enter a new question to ask something else

## 💡 Tips for Better Answers

### Good Questions:
✅ "What is the dropout voltage at 25°C at 0.6A current?"
✅ "What is the maximum value shown on the y-axis?"
✅ "At what temperature does the curve reach 0.3V?"

### Less Effective:
❌ "Tell me about this graph" (too vague)
❌ "Is this good?" (subjective)
❌ "What should I do?" (not about the graph data)

### Best Practices:
- Be specific about what value you want
- Include relevant conditions (temperature, current, etc.)
- Reference axis labels or curve names if visible
- Ask for one thing at a time

## 🔍 What AI Can See

The AI analyzes:
- ✅ Axis labels and units
- ✅ Curve labels and legends
- ✅ Data points and values
- ✅ Grid lines for estimation
- ✅ Temperature/condition markers
- ✅ Min/max values

## 🐛 Troubleshooting

### "Cannot determine from graph"
- Question asks for data not shown
- Graph quality is too low
- Labels are unclear

### Inaccurate Answer
- Try rephrasing the question
- Be more specific about which curve
- Upload higher resolution image

### No Answer Displayed
- Check backend logs for errors
- Verify API key is configured
- Check browser console for errors

## 📝 Backend Logging

When processing a question, backend shows:
```
📊 Received graph image: vout_vin_line_reg.jpg
❓ Custom question: What is the dropout voltage at 25°C at 0.6A current?
💾 Saved image to: uploads/vout_vin_line_reg.jpg

📥 Raw OpenAI Response:
================================================================================
{
  "answer": "The dropout voltage at 25°C at 0.6A current is approximately 0.25V..."
}
================================================================================

✅ Question answered successfully
```

## 🎓 Advanced Usage

### Combining with Equation Mode

1. First, extract equations (leave question blank)
2. Note the equations
3. Then ask specific questions for clarification
4. Use both modes to fully understand the graph

### Multiple Questions

- Ask one question at a time
- Click "Ask another question" after each answer
- Build understanding progressively

## 🔄 Future Enhancements

Potential improvements:
- [ ] Save question/answer history
- [ ] Export Q&A to file
- [ ] Suggest common questions based on graph type
- [ ] Multi-question mode
- [ ] Compare answers across multiple graphs

## ✅ Summary

**The custom question feature is now fully functional!**

- ✅ Text input for questions
- ✅ AI analyzes graph and answers
- ✅ Clean answer display
- ✅ Easy mode switching
- ✅ Backend logging
- ✅ Error handling

**You can now ask specific questions about graphs instead of just extracting equations!**
