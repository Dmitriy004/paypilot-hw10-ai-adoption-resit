from unittest import TestCase
from app.engines import fx, policy


class TestFxModule(TestCase):
    def setUp(self):
        # Backup original policy values to restore after tests
        self.original_rates = policy.RATES_TO_EUR.copy()
        self.original_tiers = policy.TIERS[:]
        self.original_allowance = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR.copy()
        self.original_spread_pct = policy.FX_SPREAD_PCT.copy()
        self.original_transfer_fees = policy.TRANSFER_FEES.copy()

        # Setup sample policy data for tests
        policy.RATES_TO_EUR.update({
            "USD": 1.1,
            "EUR": 1.0,
            "GBP": 0.9,
            "JPY": 130.0,
        })
        policy.TIERS[:] = ["basic", "premium"]
        policy.FX_FREE_MONTHLY_ALLOWANCE_EUR.update({
            "basic": 1000.0,
            "premium": 5000.0,
        })
        policy.FX_SPREAD_PCT.update({
            "basic": 1.0,
            "premium": 0.5,
        })
        policy.TRANSFER_FEES.update({
            "standard": (1.0, 0.5),
            "express": (5.0, 1.0),
        })

    def tearDown(self):
        # Restore original policy values
        policy.RATES_TO_EUR.clear()
        policy.RATES_TO_EUR.update(self.original_rates)
        policy.TIERS[:] = self.original_tiers
        policy.FX_FREE_MONTHLY_ALLOWANCE_EUR.clear()
        policy.FX_FREE_MONTHLY_ALLOWANCE_EUR.update(self.original_allowance)
        policy.FX_SPREAD_PCT.clear()
        policy.FX_SPREAD_PCT.update(self.original_spread_pct)
        policy.TRANSFER_FEES.clear()
        policy.TRANSFER_FEES.update(self.original_transfer_fees)

    def test_mid_rate_known_currencies(self):
        rate = fx.mid_rate("USD", "EUR")
        expected = policy.RATES_TO_EUR["USD"] / policy.RATES_TO_EUR["EUR"]
        self.assertAlmostEqual(rate, expected)

        rate = fx.mid_rate("GBP", "JPY")
        expected = policy.RATES_TO_EUR["GBP"] / policy.RATES_TO_EUR["JPY"]
        self.assertAlmostEqual(rate, expected)

    def test_mid_rate_unknown_currency_raises(self):
        with self.assertRaises(ValueError):
            fx.mid_rate("XYZ", "EUR")
        with self.assertRaises(ValueError):
            fx.mid_rate("USD", "ABC")

    def test_quote_basic_within_allowance(self):
        amount = 100.0
        tier = "basic"
        from_currency = "USD"
        to_currency = "EUR"
        allowance_used = 0.0
        quote = fx.quote(amount, from_currency, to_currency, tier, allowance_used)
        self.assertEqual(quote.tier, tier)
        self.assertTrue(quote.allowance_applied)
        self.assertEqual(quote.spread_pct, 0.0)
        self.assertAlmostEqual(quote.gross_amount, amount * fx.mid_rate(from_currency, to_currency))
        self.assertAlmostEqual(quote.final_amount, quote.gross_amount)

    def test_quote_basic_exceeds_allowance_default_spread(self):
        amount = 2000.0
        tier = "basic"
        from_currency = "USD"
        to_currency = "EUR"
        allowance_used = 900.0  # so 900 + amount_eur > 1000 allowance
        quote = fx.quote(amount, from_currency, to_currency, tier, allowance_used)
        self.assertFalse(quote.allowance_applied)
        self.assertEqual(quote.spread_pct, policy.FX_SPREAD_PCT[tier])
        self.assertGreater(quote.spread_amount, 0)
        self.assertAlmostEqual(quote.final_amount, quote.gross_amount - quote.spread_amount)

    def test_quote_basic_exceeds_allowance_override_spread(self):
        amount = 2000.0
        tier = "basic"
        from_currency = "USD"
        to_currency = "EUR"
        allowance_used = 900.0
        spread_override = 2.5
        quote = fx.quote(amount, from_currency, to_currency, tier, allowance_used,
                         spread_pct_override=spread_override)
        self.assertFalse(quote.allowance_applied)
        self.assertEqual(quote.spread_pct, spread_override)

    def test_quote_partial_allowance_applied(self):
        amount = 2000.0
        tier = "basic"
        from_currency = "USD"
        to_currency = "EUR"
        # Use partial allowance: allowance used + amount_eur > total, partial_allowance=True
        allowance_used = 900.0
        quote = fx.quote(amount, from_currency, to_currency, tier, allowance_used,
                         partial_allowance=True)
        self.assertFalse(quote.allowance_applied)
        self.assertGreater(quote.spread_amount, 0)
        # spread_amount should be less than full spread because part of allowance applies
        full_spread_amount = quote.gross_amount * policy.FX_SPREAD_PCT[tier] / 100.0
        self.assertLess(quote.spread_amount, full_spread_amount)

    def test_quote_invalid_tier_raises(self):
        with self.assertRaises(ValueError):
            fx.quote(100, "USD", "EUR", "unknown_tier")

    def test_quote_as_dict_rounding(self):
        amount = 123.456789123
        tier = "basic"
        from_currency = "USD"
        to_currency = "EUR"
        q = fx.quote(amount, from_currency, to_currency, tier)
        d = q.as_dict()
        self.assertIsInstance(d, dict)
        # All float values should be rounded to 6 decimals
        for k, v in d.items():
            if isinstance(v, float):
                self.assertEqual(round(v, 6), v)

    def test_transfer_fee_known_type(self):
        amount_eur = 1000.0
        transfer_type = "standard"
        fee_info = fx.transfer_fee(amount_eur, transfer_type)
        self.assertEqual(fee_info["transfer_type"], transfer_type)
        flat, pct = policy.TRANSFER_FEES[transfer_type]
        expected_fee = flat + amount_eur * pct / 100.0
        self.assertAlmostEqual(fee_info["total_fee_eur"], round(expected_fee, 2))
        self.assertEqual(fee_info["flat_fee_eur"], flat)
        self.assertEqual(fee_info["percent_fee"], pct)

    def test_transfer_fee_unknown_type_raises(self):
        with self.assertRaises(ValueError):
            fx.transfer_fee(100.0, "unknown_type")
