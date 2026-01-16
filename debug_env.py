from pathlib import Path

# 1. Вычисляем путь (как в config.py)
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

print(f"Checking .env at: {ENV_PATH}")

# 2. Проверяем существование
if ENV_PATH.exists():
    print("✅ File exists!")
    try:
        content = ENV_PATH.read_text(encoding="utf-8")
        print("--- Content Preview ---")
        for line in content.splitlines():
            if "DATABASE_URL" in line:
                print(f"Found DATABASE_URL: {line[:20]}...")
            if "SECRET_KEY" in line:
                print(f"Found SECRET_KEY: {line[:15]}...")
        print("---------------------")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
else:
    print("❌ File NOT found!")
    print("Listing files in directory:")
    for f in BASE_DIR.iterdir():
        if f.is_file():
            print(f" - {f.name}")
