def save_file(path: str, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ File saved to {path}")


def read_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()