# Авторське рев'ю запасного набору

Набір: tests/generated/test_fx_generated.py, 8 функцій / 15 кейсів. Критерії: prompts/review-criteria.md (заморожені до первинної генерації). Новизна — щодо авторського manual і вже прийнятих записів нижче. Числовий oracle має бути незалежним; для винятків/властивостей — N/A. Один запис на функцію, незалежно від кількості параметрів.

Таймер: **23.11.2026, 23:13:25–23:29:49 Europe/Warsaw**, **984 с = 16:24 = 16.4 хв**. Автор підтвердив відсутність перерв. У записах по функціях **144 с = 2:24**, переписування **0 с**. Решту **840 с = 14:00** автор пояснив заповненням журналу, читанням критеріїв і роботою з IDE; розподілу між цими діями не заміряно. Повна ціна review — 984 с, не 984+144. Це wall-інтервал із затримкою повідомлень, не незалежний active-only вимір. Первинний авторський журнал збережено у cea0e47b2084133a8027a4191c645ea85794ff5d до цього оформлення.

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

## Підсумок

Прийнято **8 з 8**, відхилено **0 з 8 (0%)**, переписано **0 функцій**. Усі дії as-is; змін у вихідних manual/generated немає. Основний mutation score стосується всього наданого запасного набору, а не нової генерації моделі.

## Звірка назв із замороженими критеріями

Авторські теги State, Coverage, Cross-currency, Arithmetic, Partial allowance, Override й Exceptions описують сценарій. Вони не додають нових правил до шести зафіксованих критеріїв. Відповідність для перевірки журналу:

| Запис | Застосовні критерії | Уточнення |
| --- | --- | --- |
| G-01 | Оракул; крайовий випадок; новизна | Числа 500/500.01 — точна межа tier1 і крок понад неї |
| G-02 | Рівень assertion; крайовий випадок; новизна | Використано400 + сума100 = межа500, є стан попереднього використання |
| G-03 | Оракул; рівень assertion; новизна | Явні незалежні числа за трьома тірами; точна межа тут не заявлена |
| G-04 | Оракул; рівень assertion; новизна | GBP/PLN з фіксованими коефіцієнтами, не результатами productionhelper |
| G-05 | Оракул; рівень assertion; новизна | Частково невикористаний ліміт, незалежні суми комісії та виплати |
| G-06 | Оракул; рівень assertion; новизна | Інший стан partial: залишок дорівнює нулю, комісія з усієї суми; це не твердження про exacttransactionboundary |
| G-07 | Оракул; рівень assertion; новизна | Головне правило — override всередині/поза пільгою. Входи100/600 не названі точним boundary500; критерій точної межі N/A |
| G-08 | Рівень assertion; новизна; оракул N/A | До manual додає unknown tier/target currency та точні повідомлення; частина sourcecurrency сама по собі вже була в manual |

Ця технічна звірка не змінює авторські verdicts, причини чи секунди й не рахується додатковим людським рев'ю. Поля про ім'я/незалежність не мають видимих суперечностей: функції не залежать від годинника, спільного змінного стану чи порядку.

## Технічне відхилення первинного original-red output

Окремий артефакт b69af5e26908e905ff4f2b185729aea7b27ad4e5, до запасного переходу. Підстава кожного rejected — правило original-red із заморожених критеріїв, не вигадане індивідуальне людське рев'ю. [Первинний прогін](reports/original-validation.json) доводить спільну причину: setUp, рядок21, tuple sliceassignment; testbody кожної функції не починається. Дія кожної: raw збережено в історії й архіві, для подальшого порівняння використано запасний набір. Людський час на кожну з цих10функцій **не виміряно**, не0 і не частина984с.

| ID | Первинна функція | Технічний verdict | Критерій / причина |
| --- | --- | --- | --- |
| RAW-G01 | test_mid_rate_known_currencies | rejected | original-red / setUp |
| RAW-G02 | test_mid_rate_unknown_currency_raises | rejected | original-red / setUp |
| RAW-G03 | test_quote_basic_within_allowance | rejected | original-red / setUp |
| RAW-G04 | test_quote_basic_exceeds_allowance_default_spread | rejected | original-red / setUp |
| RAW-G05 | test_quote_basic_exceeds_allowance_override_spread | rejected | original-red / setUp |
| RAW-G06 | test_quote_partial_allowance_applied | rejected | original-red / setUp |
| RAW-G07 | test_quote_invalid_tier_raises | rejected | original-red / setUp |
| RAW-G08 | test_quote_as_dict_rounding | rejected | original-red / setUp |
| RAW-G09 | test_transfer_fee_known_type | rejected | original-red / setUp |
| RAW-G10 | test_transfer_fee_unknown_type_raises | rejected | original-red / setUp |

Технічно відхилено10/10первинного output. Авторський підсумок запасного набору залишається8/8accepted,0/8rejected. Ці два різні артефакти не зведені у спільний показник відхилення18функцій.
