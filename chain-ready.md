# Перевірка відтворення

Локальний чистий git-clone джерела **d5ebffe4e65ae1ae3b5d0d50155c81eff712b2d7** перевірено 23.11.2026. Створено нову .venv, залежності встановлено через pip install -r requirements.txt.

| Команда | Фактичний результат |
| --- | --- |
| pytest tests/manual | 6 PASS |
| pytest tests/generated | 15 PASS, запасний набір |
| pytest tests/manual tests/generated | 21 PASS |
| python tools/run_mutants.py --set all | До кінця; 10/12, вціліли D-01/D-03 |

Усі команди exit0; trackedфайли clone не змінені. Побайтовий оригінал tests_backup.txt збережено без перетворення під час clone. Службовий mutationreport залишився тільки у перевірочному clone і не переноситься у джерело.

Зовнішній proof: `C:/Users/Admin/AppData/Local/Temp/paypilot-resit-fallback-clean-ntnn5xgj/proof.json`, SHA256 `a54cf84b5f2a27e8126d36bad20beed145396566b8b54c4e0aba4ef4035ff962`. Це локальний попередній контроль; публікація й фінальна перевірка саме GitHub-clone ще не виконані. Авторський review у цьому snapshot триває; початковий червоний OpenAIoutput і всі попередні докази лишаються в історії.

## Публічний GitHub-clone після завершення review

[Репозиторій](https://github.com/Dmitriy004/paypilot-hw10-ai-adoption-resit), visibilityPUBLIC, defaultbranchmain. Перевірене джерело **37dcd806dc70f98432bfc1fea8c0443fd16c6ae7** склонував саме з GitHub у нову папку, створив нову .venv й встановив requirements.

| Перевірка | Результат |
| --- | --- |
| pytest tests/manual | 6 PASS |
| pytest tests/generated | 15 PASS |
| pytest | 25 PASS:21порівняльний кейс +4окремі регресії звітного інструмента |
| python tools/run_mutants.py --set all | 10/12, D-01/D-03 вижили, uncommitted:false для списку |
| python tools/generation_summary.py reports/generation.json | Первинний output10функцій/$0.002638 і запасний8функцій розділені |

Усі команди exit0, початковий gitstatusчистий, trackedфайли після перевірок незмінні. Зовнішній proof `C:/Users/Admin/AppData/Local/Temp/paypilot-hw10-resit-github-check-l4d26pop/proof.json`, SHA256 `fd89eab46240b9b0b2d5bb5ec4a26dc415e7d050a2c3b10ec202f9823749e209`. Перевірочний report залишено тільки у clone: `reports/mutants-all-20261123-224308Z.json`; його не перенесено й не закомічено у джерело.

Цей запис описує новіший стан і не змінює попередній локальний snapshot. Подальші зміни лише текстового опису публікації/здачі не замінюють перевірене джерело. LMSвідправка підтверджується окремим записом після фактичного натискання, не самим push.
