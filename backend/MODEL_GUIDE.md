# OpenAI Model Selection Guide

## Available Models

### GPT-3.5 Turbo
- **Model Name:** `gpt-3.5-turbo`
- **Speed:** ⚡⚡⚡ Very Fast
- **Cost:** 💰 Low ($0.50 / 1M input tokens)
- **Accuracy:** ⭐⭐⭐ Good
- **Best For:** Simple parameter extraction, well-formatted datasheets
- **Context Window:** 16K tokens (~60,000 chars)

### GPT-4 Turbo
- **Model Name:** `gpt-4-turbo` or `gpt-4-turbo-preview`
- **Speed:** ⚡⚡ Fast
- **Cost:** 💰💰 Medium ($10 / 1M input tokens)
- **Accuracy:** ⭐⭐⭐⭐ Very Good
- **Best For:** Complex datasheets, better reasoning
- **Context Window:** 128K tokens (~480,000 chars)

### GPT-4o (Optimized)
- **Model Name:** `gpt-4o`
- **Speed:** ⚡⚡⚡ Very Fast
- **Cost:** 💰💰 Medium ($2.50 / 1M input tokens)
- **Accuracy:** ⭐⭐⭐⭐⭐ Excellent
- **Best For:** Best balance of speed, cost, and accuracy
- **Context Window:** 128K tokens (~480,000 chars)
- **Recommended:** ✅ Best choice for most use cases

### GPT-4
- **Model Name:** `gpt-4`
- **Speed:** ⚡ Slower
- **Cost:** 💰💰💰 High ($30 / 1M input tokens)
- **Accuracy:** ⭐⭐⭐⭐⭐ Excellent
- **Best For:** Maximum accuracy, complex reasoning
- **Context Window:** 8K tokens (~30,000 chars)

## How to Change Models

Edit your `.env` file:

```bash
# For GPT-3.5 (default, fastest, cheapest)
OPENAI_MODEL=gpt-3.5-turbo

# For GPT-4o (recommended - best balance)
OPENAI_MODEL=gpt-4o

# For GPT-4 Turbo (large context)
OPENAI_MODEL=gpt-4-turbo

# For GPT-4 (maximum accuracy)
OPENAI_MODEL=gpt-4
```

## Recommendations

### If you're getting poor results (5/16 parameters):
1. **Try GPT-4o first** - Best balance of accuracy and cost
2. **Check your datasheet** - Is it well-formatted? Are parameters clearly labeled?
3. **Try GPT-4-turbo** - If datasheet is very long or complex

### If cost is a concern:
- Start with `gpt-3.5-turbo`
- Only upgrade if results are unsatisfactory

### If accuracy is critical:
- Use `gpt-4o` or `gpt-4-turbo`
- These models have better reasoning and can handle ambiguous cases

## Testing Different Models

Run the test script to verify:
```bash
python test_openai_config.py
```

The script will show which model is being used and test extraction quality.
