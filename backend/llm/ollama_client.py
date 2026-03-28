import requests

class OllamaClient:

    def ask(self, prompt, model="llama3.1"):
        url = "http://localhost:11434/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "")
  