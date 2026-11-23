import pytest

from app.engines.fx import mid_rate, quote


def test_mid_rate_known_currency():
    result = mid_rate("EUR", "USD")

    assert result > 0


def test_mid_rate_same_currency():
    result = mid_rate("EUR", "EUR")

    assert result == 1


def test_mid_rate_unknown_currency():
    with pytest.raises(ValueError):
        mid_rate("XXX", "EUR")


def test_quote_returns_expected_fields():
    result = quote(
        amount=100,
        from_currency="EUR",
        to_currency="USD",
        tier="tier1",
    )

    assert "rate" in result
    assert "converted_amount" in result
    assert "fee" in result


def test_quote_zero_amount():
    result = quote(
        amount=0,
        from_currency="EUR",
        to_currency="USD",
        tier="tier1",
    )

    assert result["converted_amount"] == 0


def test_quote_negative_amount():
    with pytest.raises(ValueError):
        quote(
            amount=-100,
            from_currency="EUR",
            to_currency="USD",
            tier="tier1",
        )