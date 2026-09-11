from src.app import add, greet, multiply


def test_add():
    assert add(2, 3) == 5


def test_greet():
    assert greet("DevOps") == "Hello, DevOps!"


def test_multiply():
    assert multiply(2, 3) == 6
