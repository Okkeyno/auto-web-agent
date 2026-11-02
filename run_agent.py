
# run_agent.py

import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# First load the environment variables
load_dotenv()

# API key validation
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )

# Import the agent
from app.agent import run_agent


print("=" * 45)
print("       Automated Web Agent")
print("          GEMINI AI")
print("=" * 45)

task = input("\nProvide a task for the agent: ")

if not task.strip():
    raise ValueError("Task cannot be empty.")

with sync_playwright() as playwright:

    browser = playwright.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    try:

        page.goto(
            "http://localhost:8000",
            wait_until="domcontentloaded"
        )

        print("\nBrowser opened.")
        print("Task analysis in progress...")

        run_agent(page, task)

    finally:

        browser.close()

        print("\nBrowser closed.")
