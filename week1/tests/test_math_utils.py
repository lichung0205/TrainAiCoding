# tests/test_math_utils.py
import math
import pytest
import src.math_utils as mu

# --- 基本運算 ---


@pytest.mark.parametrize(
    "a,b,ans",
    [
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
        (2.5, 0.5, 3.0),
    ],
)
def test_add(a, b, ans):
    assert mu.add(a, b) == pytest.approx(ans)


@pytest.mark.parametrize(
    "a,b,ans",
    [
        (5, 3, 2),
        (-1, -4, 3),
        (2.5, 0.5, 2.0),
    ],
)
def test_subtract(a, b, ans):
    assert mu.subtract(a, b) == pytest.approx(ans)


@pytest.mark.parametrize(
    "a,b,ans",
    [
        (4, 6, 24),
        (-3, 5, -15),
        (2.5, 0.2, 0.5),
    ],
)
def test_multiply(a, b, ans):
    assert mu.multiply(a, b) == pytest.approx(ans)


@pytest.mark.parametrize(
    "a,b,ans",
    [
        (10, 2, 5),
        (7.5, 2.5, 3.0),
    ],
)
def test_divide(a, b, ans):
    assert mu.divide(a, b) == pytest.approx(ans)


def test_divide_by_zero_raises_value_error():
    # math_utils.divide 對除數為 0 會拋 ValueError（驗證規格）。 :contentReference[oaicite:2]{index=2}
    with pytest.raises(ValueError):
        mu.divide(1, 0)


# --- 進階功能 ---


@pytest.mark.parametrize(
    "base, exp, ans",
    [
        (2, 10, 1024),
        (9, 0.5, 3.0),
        (5, 0, 1),
    ],
)
def test_power(base, exp, ans):
    assert mu.power(base, exp) == pytest.approx(ans)


@pytest.mark.parametrize("n", [0, 2, 12, -4, 100])
def test_is_even_true(n):
    assert mu.is_even(n) is True


@pytest.mark.parametrize("n", [1, 3, 15, -7, 101])
def test_is_even_false(n):
    assert mu.is_even(n) is False


# --- 常數與代數性質 ---


def test_commutativity_add_and_multiply():
    pairs = [(3, 5), (2.5, 7), (-4, 10)]
    for a, b in pairs:
        assert mu.add(a, b) == mu.add(b, a)
        assert mu.multiply(a, b) == mu.multiply(b, a)
