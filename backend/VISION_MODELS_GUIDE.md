# Vision Models Guide for Graph Analysis

## Recommended Vision Models on OpenRouter

### 1. **Google Gemini Pro Vision** (Recommended)
```env
OPENROUTER_VISION_MODEL=google/gemini-pro-vision
```
- ✅ **Free tier available**
- ✅ Good at chart and graph analysis
- ✅ Fast response times
- ✅ Reliable availability
- 💰 Cost-effective

### 2. **OpenAI GPT-4 Vision Preview**
```env
OPENROUTER_VISION_MODEL=openai/gpt-4-vision-preview
```
- ✅ Excellent accuracy
- ✅ Great for technical diagrams
- ✅ High reliability
- 💰 Higher cost
- ⚠️ Requires OpenAI credits

### 3. **Anthropic Claude 3.5 Sonnet**
```env
OPENROUTER_VISION_MODEL=anthropic/claude-3-5-sonnet
```
- ✅ Excellent for technical analysis
- ✅ Great at understanding complex graphs
- ✅ Good reasoning capabilities
- 💰 Moderate cost

### 4. **Qwen VL Plus**
```env
OPENROUTER_VISION_MODEL=qwen/qwen-vl-plus
```
- ✅ Good for charts and diagrams
- ✅ Cost-effective
- ⚠️ May have availability issues

### 5. **01.AI Yi Vision**
```env
OPENROUTER_VISION_MODEL=01-ai/yi-vision
```
- ✅ Designed for complex visual tasks
- ✅ Good for multilingual documents
- ⚠️ **Currently experiencing availability issues**
- ⚠️ May not be available in all regions

## Troubleshooting

### Error: "No endpoints found for [model-name]"

This error means the model is not currently available. Try these solutions:

1. **Switch to a different model** (recommended):
   ```env
   OPENROUTER_VISION_MODEL=google/gemini-pro-vision
   ```

2. **Check model availability** at: https://openrouter.ai/models
   - Filter by "Image" input modality
   - Check the model status

3. **Verify your OpenRouter API key** has credits

4. **Check regional availability** - some models may not be available in your region

### Error: "401 Unauthorized"

- Check your API key is correct in `.env`
- Verify you have credits in your OpenRouter account
- Make sure `API_PROVIDER=openrouter` is set

## Testing Vision Models

You can test different models by:

1. Update your `.env` file:
   ```env
   API_PROVIDER=openrouter
   OPENROUTER_API_KEY=your-key-here
   OPENROUTER_VISION_MODEL=google/gemini-pro-vision
   ```

2. Restart the backend server

3. Upload a test graph image in the Graph Analysis tab

4. Compare results from different models

## Cost Comparison (Approximate)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Best For |
|-------|----------------------|------------------------|----------|
| Gemini Pro Vision | $0.125 | $0.375 | Budget-friendly |
| GPT-4 Vision | $10.00 | $30.00 | High accuracy |
| Claude 3.5 Sonnet | $3.00 | $15.00 | Technical analysis |
| Qwen VL Plus | $0.50 | $1.50 | Cost-effective |

*Note: Prices are approximate and may change. Check OpenRouter for current pricing.*

## Best Practices

1. **Start with Gemini Pro Vision** - it's free tier makes it great for testing
2. **Use GPT-4 Vision** for production/critical analysis
3. **Try Claude 3.5 Sonnet** for complex technical graphs
4. **Keep backup models** configured in case primary is unavailable

## Current Status (as of Nov 2025)

- ✅ **Working**: google/gemini-pro-vision, openai/gpt-4-vision-preview, anthropic/claude-3-5-sonnet
- ⚠️ **Issues**: 01-ai/yi-vision (endpoint availability problems)
- 📝 **Check**: https://openrouter.ai/models for real-time status
