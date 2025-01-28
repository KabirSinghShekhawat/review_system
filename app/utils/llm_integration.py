from openai import OpenAI

from app.config import settings

client = OpenAI(api_key=settings.OPENAI_KEY)


def analyze_tone_and_sentiment(text: str, stars: int):
    return "positive", "positive"
    response = client.completions.create(
        model="gpt-4o-mini",
        prompt=f"Analyze the tone and sentiment of this review: {text}. Stars: {stars}",
        max_tokens=50,
    )
    result = response.choices[0].text.strip()
    tone, sentiment = result.split(", ")
    return tone, sentiment
