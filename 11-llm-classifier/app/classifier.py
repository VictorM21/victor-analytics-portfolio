import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in .env file")

client = Groq(api_key=GROQ_API_KEY)

def classify_product(description: str) -> dict:
    prompt = f"""You are a product classification system.

Classify the following product into exactly one category: Electronics, Clothing, Home, Beauty, Sports.

Return ONLY a valid JSON object with three fields:
- "category": the chosen category
- "confidence": a number from 0.0 to 1.0 (how certain you are)
- "reasoning": a one‑sentence explanation

Examples:
Product: "Wireless noise‑cancelling headphones" -> {{"category": "Electronics", "confidence": 0.98, "reasoning": "Clearly an electronic audio device."}}
Product: "Men's cotton running shorts" -> {{"category": "Sports", "confidence": 0.95, "reasoning": "Athletic apparel for sports use."}}
Product: "Ceramic non‑stick frying pan" -> {{"category": "Home", "confidence": 0.97, "reasoning": "Kitchen cookware for home use."}}

Now classify:
Product: {description}
JSON output:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=150,
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content.strip()
    try:
        result = json.loads(raw)
        return {
            "category": result.get("category", "Unknown"),
            "confidence": float(result.get("confidence", 0.5)),
            "reasoning": result.get("reasoning", "No reasoning provided.")
        }
    except (json.JSONDecodeError, KeyError, ValueError):
        return {
            "category": "Unknown",
            "confidence": 0.0,
            "reasoning": f"Parse error — raw output: {raw[:100]}"
        }