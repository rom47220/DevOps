"""Mini calculatrice pour le projet Devsecops."""


def add(a: int, b: int) -> int:
    """Return the sum of a and b."""
    result = a + b
    return result


def multiply(a: int, b: int) -> int:
    """Return the product of a and b."""
    return a * b


def subtract(a: int, b: int) -> int:
    """Return a minus b."""
    return a - b


def greet(name: str) -> str:
    """Return a friendly greeting for name."""
    return f"Hello, {name}!"
