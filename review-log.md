# Авторське рев'ю запасного набору

Набір: tests/generated/test_fx_generated.py, 8 функцій / 15 кейсів. Критерії: prompts/review-criteria.md (заморожені до первинної генерації). Новизна — щодо авторського manual і вже прийнятих записів нижче. Числовий oracle має бути незалежним; для винятків/властивостей — N/A. Один запис на функцію, незалежно від кількості параметрів.

Таймер ще не запущений. Перед початком повідомити «починаю рев'ю»; після збереження — «рев'ю готове». У кожному записі вказати фактичні секунди перегляду; переписування окремо. Якщо не переписували — 0. Якщо час не засікали — «не виміряно», без оцінок. Переписаний код — лише tests/rewritten/, вихідні manual/generated не змінювати.

## G-01 · test_tier1_allowance_exact_boundary_and_one_cent_over
Verdict: accepted
Критерій: Boundary / Oracle
Причина: Перевіряє точну межу 500 EUR і перевищення на 0.01 EUR
Дія: as-is
Рев'ю, секунд: 23
Переписування, секунд: 0

## G-02 · test_allowance_used_before_is_included_in_limit_check
Verdict: accepted
Критерій: Boundary / State / Assertion strength
Причина: Перевіряє врахування вже використаних 400 EUR у ліміті та перехід з 100.00 на 100.01
Дія: as-is
Рев'ю, секунд: 9
Переписування, секунд: 0

## G-03 · test_tier_specific_spread_when_free_limit_exceeded
Verdict: accepted
Критерій: Oracle / Coverage
Причина: Три тарифи з фіксованими очікуваними лімітами та ставками 1.5/0.9/0.5
Дія: as-is
Рев'ю, секунд: 16
Переписування, секунд: 0

## G-04 · test_cross_currency_conversion_uses_both_eur_rates
Verdict: accepted
Критерій: Oracle / Cross-currency
Причина: Фіксовані коефіцієнти 1.17 та 0.23 для GBP→PLN дають незалежний від виклику production-функцій розрахунок
Дія: as-is
Рев'ю, секунд: 17
Переписування, секунд: 0

## G-05 · test_partial_allowance_charges_only_exceeding_portion
Verdict: accepted
Критерій: Arithmetic / Partial allowance
Причина: Для 400 використаних із 500 EUR і транзакції 200 EUR перевірено спред лише з перевищення 100 EUR: 1.5 EUR, final 198.5
Дія: as-is
Рев'ю, секунд: 12
Переписування, секунд: 0

## G-06 · test_partial_allowance_after_limit_exhausted_charges_full_amount
Verdict: accepted
Критерій: Boundary / Partial allowance
Причина: Перевіряє вичерпаний ліміт (used=500): повні 200 EUR обкладаються спредом 3 EUR, final 197 EUR
Дія: as-is
Рев'ю, секунд: 10
Переписування, секунд: 0

## G-07 · test_spread_override_applies_only_outside_free_allowance
Verdict: accepted
Критерій: Override / Boundary / Oracle
Причина: Два сценарії: override 2% ігнорується в межах ліміту та застосовується поза ним
Дія: as-is
Рев'ю, секунд: 25
Переписування, секунд: 0

## G-08 · test_unknown_tier_or_currency_raises_value_error
Verdict: accepted
Критерій: Exceptions (Oracle N/A) / Coverage
Причина: Перевіряє ValueError і конкретні повідомлення для невідомого tier, source currency і target currency
Дія: as-is
Рев'ю, секунд: 32
Переписування, секунд: 0
