import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def ask(self, prompt: str):

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # 🔥 STRONGEST MODEL
            messages=[
                {
                    "role": "system",
                    "content": """
You are an MSME business analyst.

You analyze business opportunities ONLY using the data provided.

Rules:
- Never invent statistics
- Never mention averages
- Never mention other cities
- Only analyze the specific city provided
- Use only the numbers given in the input
- If data is missing, say "data not available"

Explain results clearly for entrepreneurs.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,   # lower = more factual
            max_tokens=600
        )

        return response.choices[0].message.content