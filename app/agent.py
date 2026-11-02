
import os
from pathlib import Path

from google import genai
from google.genai import types

from app.browser_tools import (
    inspect_page,
    fill_form_field,
    submit_contact_form
)

import time
import random


def send_message_with_retry(chat, task, max_retries=3):

    for attempt in range(max_retries):

        try:
            print(
                f"\n[GEMINI] İstek gönderiliyor. "
                f"Deneme: {attempt + 1}/{max_retries}"
            )

            response = chat.send_message(task)

            return response

        except Exception as error:

            error_message = str(error).upper()

            retryable = any(
                code in error_message
                for code in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "502",
                    "504",
                    "DEADLINE_EXCEEDED"
                ]
            )

            if not retryable:
                raise

            if attempt == max_retries - 1:
                raise

            delay = (2 ** (attempt + 1)) + random.uniform(0, 1)

            print(
                f"\n[GEMINI] Geçici API hatası: {error}"
            )

            print(
                f"[GEMINI] {delay:.1f} saniye sonra tekrar denenecek."
            )

            time.sleep(delay)


def run_agent(page, task):

    # 1. Gemini API bağlantısı
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY bulunamadı. .env dosyasını kontrol et."
        )

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=300000
        )
    )

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    # 2. System prompt dosyasını oku
    base_dir = Path(__file__).resolve().parent.parent
    prompt_path = base_dir / "prompts" / "system_prompt.txt"

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"System prompt bulunamadı: {prompt_path}"
        )

    system_prompt = prompt_path.read_text(
        encoding="utf-8"
    )

    # 3. Tarayıcı araçlarını tanımla

    def inspect_page_tool() -> dict:
        """Inspect the current web page and return its content."""

        print("\n[AGENT] Sayfa inceleniyor...")

        result = inspect_page(page)

        print("[AGENT] Sayfa incelemesi tamamlandı.")

        return result

    def fill_form_field_tool(
        field: str,
        value: str
    ) -> dict:
        """Fill and verify a contact form field."""

        print(f"\n[AGENT] {field} alanı dolduruluyor...")

        result = fill_form_field(
            page,
            field,
            value
        )

        if result.get("success"):
            print(f"[AGENT] {field} alanı doğrulandı.")
        else:
            print(f"[AGENT] Hata: {result.get('error')}")

        return result

    def submit_contact_form_tool() -> dict:
        """Request user confirmation before submitting the contact form."""

        print("\n[AGENT] Form gönderimi için onay bekleniyor...")

        return submit_contact_form(page)

    tools = [
        inspect_page_tool,
        fill_form_field_tool,
        submit_contact_form_tool
    ]

    # 4. Gemini sohbetini başlat
    print("\n================================")
    print("AUTONOMOUS WEB AGENT")
    print("================================")
    print(f"Model: {model}")
    print("Görev analiz ediliyor...")

    try:

        chat = client.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=tools
            )
        )

        # 5. Kullanıcı görevini Gemini'ye gönder
        response = send_message_with_retry(chat, task)

        # 6. Sonucu göster
        result = response.text or "Gemini boş bir yanıt döndürdü."

        print("\n========== AGENT RESPONSE ==========")
        print(result)
        print("====================================")

        return result

    except Exception as error:

        print("\n========== AGENT ERROR ==========")
        print("Hata türü:", type(error).__name__)
        print("Hata açıklaması:", error)
        print("=================================")

        return f"Agent error: {type(error).__name__}: {error}"
