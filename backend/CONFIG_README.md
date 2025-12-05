# API Configuration Guide

This application supports both **OpenAI** and **OpenRouter** APIs for:
- AI-powered parameter extraction (text models)
- Graph analysis with vision models (image understanding)

## Quick Start

1. **Copy the example environment file:**
   ```bash
   copy .env.example .env
   ```

2. **Choose your API provider** by editing `.env`:
   - Set `API_PROVIDER=openai` for OpenAI
   - Set `API_PROVIDER=openrouter` for OpenRouter

3. **Add your API key** for the chosen provider

4. **Restart the backend server**

## Configuration Options

### API Provider Selection

```env
API_PROVIDER=openai  # or 'openrouter'
```

### OpenAI Configuration

```env
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

**Get API Key:** https://platform.openai.com/api-keys

**Available Models:**
- `gpt-3.5-turbo` (recommended for cost-effectiveness)
- `gpt-4` (better accuracy, higher cost)
- `gpt-4-turbo-preview` (faster GPT-4)

### OpenRouter Configuration

```env
OPENROUTER_API_KEY=sk-or-your-key-here
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```

**Get API Key:** https://openrouter.ai/keys

**Popular Models:**
- `openai/gpt-3.5-turbo` - Fast and cost-effective
- `openai/gpt-4` - High accuracy
- `anthropic/claude-3-opus` - Excellent for technical documents
- `google/gemini-pro` - Good balance of speed and accuracy
- `meta-llama/llama-3-70b-instruct` - Open source alternative

**Full Model List:** https://openrouter.ai/models

### Common Settings

```env
TEMPERATURE=0.1      # Lower = more deterministic (0.0-1.0)
MAX_TOKENS=2000      # Maximum response length
```

## Why Use OpenRouter?

OpenRouter provides several advantages:

1. **Multiple Models:** Access to 100+ AI models from different providers
2. **Cost Optimization:** Compare prices and choose the best model for your budget
3. **Fallback Options:** Automatically switch models if one is unavailable
4. **No Vendor Lock-in:** Easy to switch between different AI providers

## Checking Configuration

You can check your current configuration by calling the API endpoint:

```bash
curl http://localhost:8000/api/config
```

Response example:
```json
{
  "success": true,
  "config": {
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "base_url": "https://api.openai.com/v1",
    "temperature": 0.1,
    "max_tokens": 2000,
    "has_api_key": true
  },
  "is_valid": true,
  "error": null
}
```

## Troubleshooting

### Error: "API key not provided"
- Make sure you've created a `.env` file from `.env.example`
- Check that the API key is set for your chosen provider
- Verify there are no extra spaces in the key

### Error: "Invalid API_PROVIDER"
- `API_PROVIDER` must be either `openai` or `openrouter` (lowercase)

### Error: "Model not found"
- For OpenAI: Check available models at https://platform.openai.com/docs/models
- For OpenRouter: Verify model name at https://openrouter.ai/models
- Model names are case-sensitive

## Example Configurations

### Configuration 1: OpenAI GPT-3.5 (Cost-Effective)
```env
API_PROVIDER=openai
OPENAI_API_KEY=sk-proj-abc123...
OPENAI_MODEL=gpt-3.5-turbo
TEMPERATURE=0.1
MAX_TOKENS=2000
```

### Configuration 2: OpenRouter with Claude (High Quality)
```env
API_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-xyz789...
OPENROUTER_MODEL=anthropic/claude-3-opus
TEMPERATURE=0.1
MAX_TOKENS=2000
```

### Configuration 3: OpenRouter with Llama (Open Source)
```env
API_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-xyz789...
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct
TEMPERATURE=0.1
MAX_TOKENS=2000
```

## Security Notes

- **Never commit `.env` file to version control** (it's in `.gitignore`)
- Keep your API keys confidential
- Rotate keys regularly
- Use environment-specific keys for development/production
