from src.app import add, subtract, greet


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_greet():
    assert greet("DevOps") == "Hello, DevOps!"
