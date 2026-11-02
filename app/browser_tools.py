
def inspect_page(page):
    """Web sayfasının başlığını, adresini ve içeriğini inceler."""

    title = page.title()
    url = page.url
    content = page.locator("body").inner_text()

    return {
        "success": True,
        "title": title,
        "url": url,
        "content": content[:5000],
        "available_fields": [
            "name",
            "email",
            "subject",
            "message"
        ]
    }


def fill_form_field(page, field, value):
    """Belirtilen form alanını doldurur ve doğrular."""

    fields = {
        "name": "#name",
        "email": "#email",
        "subject": "#subject",
        "message": "#message"
    }

    if field not in fields:
        return {
            "success": False,
            "error": "Invalid field"
        }

    if not isinstance(value, str) or not value.strip():
        return {
            "success": False,
            "error": "Invalid or empty value"
        }

    locator = page.locator(fields[field])

    locator.fill(value)

    actual_value = locator.input_value()

    if actual_value != value:
        return {
            "success": False,
            "error": "Field validation failed"
        }

    return {
        "success": True,
        "field": field,
        "value": actual_value,
        "message": "Field filled successfully"
    }


def submit_contact_form(page):
    """Kullanıcı onayıyla iletişim formunu gönderir."""

    fields = {
        "name": "#name",
        "email": "#email",
        "subject": "#subject",
        "message": "#message"
    }

    # Önce bütün alanları kontrol et.
    for field, selector in fields.items():

        value = page.locator(selector).input_value()

        if not value.strip():
            return {
                "success": False,
                "error": f"Missing form field: {field}"
            }

    # Gönderim öncesi kullanıcıya özet göster.
    print("\n========== FORM ÖZETİ ==========")

    for field, selector in fields.items():
        value = page.locator(selector).input_value()
        print(f"{field}: {value}")

    print("================================")

    confirmation = input(
        "\nFormu göndermek istiyor musunuz? (Y/N): "
    )

    if confirmation.strip().lower() != "y":
        return {
            "success": False,
            "message": "User cancelled the submission."
        }

    # Kullanıcı onayladıysa gönder.
    page.locator(
        "#contact-form button[type='submit']"
    ).click()

    page.locator("#success-message").wait_for(
        state="visible",
        timeout=5000
    )

    return {
        "success": True,
        "message": page.locator(
            "#success-message"
        ).inner_text()
    }


def execute_tool(name, arguments, page):
    """Gemini tarafından istenen aracı çalıştırır."""

    if page.url != "http://localhost:8000/":
        return {
            "success": False,
            "error": "Unauthorized page"
        }

    if name == "inspect_page":

        return inspect_page(page)

    elif name == "fill_form_field":

        return fill_form_field(
            page,
            arguments["field"],
            arguments["value"]
        )

    elif name == "submit_contact_form":

        return submit_contact_form(page)

    else:

        return {
            "success": False,
            "error": "Unknown tool"
        }
