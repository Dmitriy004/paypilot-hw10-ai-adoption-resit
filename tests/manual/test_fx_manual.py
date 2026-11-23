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

    assert result.from_currency == "EUR"
    assert result.to_currency == "USD"
    assert result.amount == 100
    assert result.mid_rate > 0
    assert result.final_amount == pytest.approx(
        result.gross_amount - result.spread_amount
    )


def test_quote_zero_amount():
    result = quote(
        amount=0,
        from_currency="EUR",
        to_currency="USD",
        tier="tier1",
    )

    assert result.gross_amount == 0
    assert result.spread_amount == 0
    assert result.final_amount == 0


def test_quote_negative_amount():
    result = quote(
        amount=-100,
        from_currency="EUR",
        to_currency="USD",
        tier="tier1",
    )

    assert result.amount == -100
    assert result.gross_amount == pytest.approx(
        -100 * result.mid_rate
    )
    assert result.final_amount == pytest.approx(
        result.gross_amount - result.spread_amount
    )
