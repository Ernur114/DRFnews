# API Эндпоинты

## Аутентификация / пользователи

* **POST /auth/register/** — регистрация пользователя (создаётся с `is_active = false`, отправляется код активации).
* **POST /auth/activate/** — активация аккаунта по email и коду.
* **POST /auth/token/** — получение JWT access/refresh токенов.
* **POST /auth/token/refresh/** — обновление access-токена.

## Статьи

* **POST /articles/update/** — подтянуть свежие статьи из NewsAPI, сохранить новые, результат в кэш на 30 минут.
* **GET /articles/** — список статей, фильтры: `fresh=true` (за последние 24 часа), `title_contains=...`. Ответ кэшируется на 10 минут.
