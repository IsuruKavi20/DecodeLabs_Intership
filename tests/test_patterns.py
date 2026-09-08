import pytest

from src.patterns import (
    has_keyboard_walk,
    has_sequential_pattern,
    has_weak_pattern,
)


@pytest.mark.parametrize("pw", ["abc", "abc123", "xyz789", "pqr"])
def test_ascending_sequences(pw):
    assert has_sequential_pattern(pw) is True


@pytest.mark.parametrize("pw", ["cba", "321", "zyx", "fedcba"])
def test_descending_sequences(pw):
    assert has_sequential_pattern(pw) is True


@pytest.mark.parametrize("pw", ["aaa", "aaa111", "brrr"])
def test_repeated_chars(pw):
    assert has_sequential_pattern(pw) is True


@pytest.mark.parametrize(
    "pw",
    ["qwerty", "asdfGH", "ZXCVBN", "1qaz2wsx", "ytrewq", "hunterqwertyx"],
)
def test_keyboard_walks(pw):
    assert has_keyboard_walk(pw) is True


@pytest.mark.parametrize(
    "pw",
    ["qwerty", "cba321", "aaa", "MyDog$Fluffy2024asdfgh"],
)
def test_has_weak_pattern_true(pw):
    assert has_weak_pattern(pw) is True


@pytest.mark.parametrize("pw", ["xK9mLp2qR", "vivid-marmoset-truck", "Blue7Sky!"])
def test_no_pattern(pw):
    assert has_sequential_pattern(pw) is False
    assert has_keyboard_walk(pw) is False
    assert has_weak_pattern(pw) is False
