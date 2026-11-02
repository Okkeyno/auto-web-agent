
from playwright.sync_api import sync_playwright

# Playwright start
with sync_playwright() as playwright:

    # Open Chromium browser
    browser = playwright.chromium.launch(
        headless=False
    )

    # New browser tab
    page = browser.new_page()

    # Open the local test site
    page.goto("http://localhost:8000")

    # Read the page title
    title = page.title()

    print("Page title:", title)

    # Find the heading on the page
    heading = page.locator("h1").inner_text()

    print("Page heading:", heading)

    # Fill the form fields
    page.locator("#name").fill("Okan Bey")

    page.locator("#email").fill("okansemercioglu@gmail.com")

    page.locator("#subject").fill("Product Information Request")

    page.locator("#message").fill(
        "I would like to get information about your products."
    )

    print("Form fields filled!")

    # Close the browser after 3 seconds
    page.wait_for_timeout(3000)

    browser.close()
