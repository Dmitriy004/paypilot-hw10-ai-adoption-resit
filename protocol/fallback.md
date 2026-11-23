# Запасний набір

Для продовження використано наданий `tests_backup.txt` як запасний comparator. Джерело і контрольні суми — [reports/fallback-source.json](../reports/fallback-source.json); незмінний вхід збережено в [artifacts/mentor-fallback/tests_backup.txt](../artifacts/mentor-fallback/tests_backup.txt). Код логічно не редагується; лише закінчення рядків робочого Pythonфайла приведено до LF згідно з налаштуванням репозиторію.

Невдалий первинний OpenAIoutput збережений у **b69af5e26908e905ff4f2b185729aea7b27ad4e5**, у reports/generation*.json і додатково як [архів коду](../artifacts/failed-generation/test_fx_generated.py.txt), поза pytestcollection. Новий файл у tests/generated — **запасний**; метадані запиту OpenAI описують тільки невдалий первинний output. Час/вартість створення запасного файла не виміряні, не запозичуються з OpenAI або старих таймерів.

Зберегти авторський manual f0340dd, список717e692, критерії98b2a2c й обидва попередні прогнози без змін. Окремий прогноз для наданого запасного набору закомітити до його прогонів. Авторське рев'ю проводиться з реальним таймером; невиміряні хвилини не заповнюються оцінками.
