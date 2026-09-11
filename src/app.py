"""Mini calculatrice pour le projet."""


def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> str:
    if not name.strip():
        raise ValueError("name must not be empty")
    return f"Hello, {name}!"
