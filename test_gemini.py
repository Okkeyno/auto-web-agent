
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={
        "api_version": "v1",
        "timeout": 300000
    }
)

model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

print("Gemini Interactions API test ediliyor...", flush=True)

try:
    interaction = client.interactions.create(
        model=model,
        input="Sadece MERHABA yaz."
    )

    print("\nAPI BAŞARILI!")
    print("Gemini yanıtı:", interaction.output_text)

except Exception as error:
    print("\nAPI HATASI:")
    print(type(error).__name__)
    print(error)
