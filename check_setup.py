
from importlib.metadata import version

packages = [
    "streamlit",
    "playwright",
    "openai",
    "pandas",
    "pytest",
    "python-dotenv"
]

print("Kurulum kontrolü başladı!\n")

for package in packages:
    try:
        print(f"{package}: {version(package)}")
    except Exception as error:
        print(f"{package}: HATA - {error}")

print("\nKurulum kontrolü tamamlandı!")
