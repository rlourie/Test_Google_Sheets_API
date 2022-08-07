# Test_Google_Sheets_API.

Для запуска тестов добавьте в tests файл авторизации сервисного аккаунта tests-358414-baea7a149cfb.json

Команда

```
pytest
```

-------

## Для создания allure отчета

```
pytest --alluredir results
allure serve results
```

-------

## Баг репорт

### ID: 001

### Метод SpreadsheetAPI.insert возвращает None (test_09)

### Cценарий:

1.Сделать вставку в таблицу

![img_1.png](img_1.png)

Ожидаемый результат: SpreadsheetAPI.insert возвращает True

Фактический результат: SpreadsheetAPI.insert возвращает None
