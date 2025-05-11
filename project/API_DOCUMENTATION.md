# Документация API

## Базовый URL
```
http://localhost:8000/api/
```

## Аутентификация

API использует аутентификацию JWT (JSON Web Token). Все эндпоинты, кроме регистрации и входа пользователя, требуют аутентификации.

### Получение JWT токена

Для аутентификации необходимо:

1. Зарегистрировать пользователя (если он еще не зарегистрирован)
2. Получить JWT токен, войдя в систему
3. Включить токен в заголовок Authorization для всех защищенных эндпоинтов

#### Регистрация пользователя
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "email": "test@example.com"
  }'
```

#### Вход и получение токена
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

Ответ:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Обновление токена
Когда токен доступа истекает (через 60 минут), вы можете получить новый, используя refresh токен:

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

### Использование токена

Для всех защищенных эндпоинтов включите токен доступа в заголовок Authorization:

```bash
curl -X GET http://localhost:8000/api/diet-types/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## Эндпоинты

### Пользователи

#### Создание пользователя (Регистрация - Аутентификация не требуется)
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "email": "test@example.com"
  }'
```

#### Получение пользователя (Требуется аутентификация)
```bash
curl -X GET http://localhost:8000/api/users/{user_id}/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Обновление пользователя (Требуется аутентификация)
```bash
curl -X PATCH http://localhost:8000/api/users/{user_id}/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{
    "weight": 75.0,
    "height": 180
  }'
```

#### Удаление пользователя (Требуется аутентификация)
```bash
curl -X DELETE http://localhost:8000/api/users/{user_id}/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### Планы питания (Все требуют аутентификации)

#### Создание плана питания
```bash
curl -X POST http://localhost:8000/api/meal-plans/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{
    "user_id": 1,
    "duration": 14,
    "total_price": 1000.0
  }'
```

#### Получение плана питания
```bash
curl -X GET http://localhost:8000/api/meal-plans/{meal_plan_id}/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### Блюда (Все требуют аутентификации)

#### Создание блюда
```bash
curl -X POST http://localhost:8000/api/meals/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{
    "name": "Healthy Salad",
    "price": 15.99,
    "description": "Fresh vegetables with olive oil",
    "diet_type_id": 1
  }'
```

#### Получение блюда
```bash
curl -X GET http://localhost:8000/api/meals/{meal_id}/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### Ингредиенты (Все требуют аутентификации)

#### Создание ингредиента
```bash
curl -X POST http://localhost:8000/api/ingredients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{
    "name": "Chicken Breast",
    "price_per_unit": 10.99,
    "unit": "kg",
    "store_name": "Local Market"
  }'
```

#### Получение ингредиента
```bash
curl -X GET http://localhost:8000/api/ingredients/{ingredient_id}/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### Типы диет (Все требуют аутентификации)

#### Создание типа диеты
```bash
curl -X POST http://localhost:8000/api/diet-types/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{
    "name": "Vegetarian",
    "is_restricted": true,
    "description": "No meat products"
  }'
```

#### Получение типа диеты
```bash
curl -X GET http://localhost:8000/api/diet-types/{diet_type_id}/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### Избранное (Все требуют аутентификации)

#### Создание избранного
```bash
curl -X POST http://localhost:8000/api/favorites/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{
    "user_id": 1,
    "meal_id": 1
  }'
```

#### Получение избранного
```bash
curl -X GET http://localhost:8000/api/favorites/{favorite_id}/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## Коллекция Postman

Вы можете импортировать следующую коллекцию в Postman:

```json
{
  "info": {
    "name": "Meal Planning API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Аутентификация",
      "item": [
        {
          "name": "Регистрация пользователя",
          "request": {
            "method": "POST",
            "url": "http://localhost:8000/api/users/",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"username\": \"testuser\",\n  \"password\": \"testpass123\",\n  \"email\": \"test@example.com\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            }
          }
        },
        {
          "name": "Получение JWT токена",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "var jsonData = pm.response.json();",
                  "pm.environment.set(\"access_token\", jsonData.access);",
                  "pm.environment.set(\"refresh_token\", jsonData.refresh);"
                ],
                "type": "text/javascript"
              }
            }
          ],
          "request": {
            "method": "POST",
            "url": "http://localhost:8000/api/token/",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"username\": \"testuser\",\n  \"password\": \"testpass123\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            }
          }
        },
        {
          "name": "Обновление токена",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "var jsonData = pm.response.json();",
                  "pm.environment.set(\"access_token\", jsonData.access);"
                ],
                "type": "text/javascript"
              }
            }
          ],
          "request": {
            "method": "POST",
            "url": "http://localhost:8000/api/token/refresh/",
            "body": {
              "mode": "raw",
              "raw": "{\n  \"refresh\": \"{{refresh_token}}\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            }
          }
        }
      ]
    },
    {
      "name": "Пользователи",
      "item": [
        {
          "name": "Получение пользователя",
          "request": {
            "method": "GET",
            "url": "http://localhost:8000/api/users/{{user_id}}/",
            "auth": {
              "type": "bearer",
              "bearer": [
                {
                  "key": "token",
                  "value": "{{access_token}}",
                  "type": "string"
                }
              ]
            }
          }
        }
      ]
    },
    {
      "name": "Планы питания",
      "item": [
        {
          "name": "Создание плана питания",
          "request": {
            "method": "POST",
            "url": "http://localhost:8000/api/meal-plans/",
            "auth": {
              "type": "bearer",
              "bearer": [
                {
                  "key": "token",
                  "value": "{{access_token}}",
                  "type": "string"
                }
              ]
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"user_id\": 1,\n  \"duration\": 14,\n  \"total_price\": 1000.0\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            }
          }
        }
      ]
    }
  ]
}
```

## Тестирование с помощью Postman

1. Скачайте и установите [Postman](https://www.postman.com/downloads/)
2. Импортируйте предоставленную выше коллекцию
3. Создайте окружение в Postman с следующими переменными:
   - `base_url`: http://localhost:8000/api
   - `access_token`: (будет установлен автоматически после входа)
   - `refresh_token`: (будет установлен автоматически после входа)
   - `user_id`: (будет установлен после создания пользователя)
   - `meal_plan_id`: (будет установлен после создания плана питания)
   - `meal_id`: (будет установлен после создания блюда)
   - `ingredient_id`: (будет установлен после создания ингредиента)
   - `diet_type_id`: (будет установлен после создания типа диеты)
   - `favorite_id`: (будет установлен после создания избранного)

4. Запустите сервер Django:
```bash
python manage.py runserver
```

5. Выполните запросы в следующем порядке:
   - Зарегистрируйте пользователя
   - Получите JWT токен (вход)
   - Используйте другие эндпоинты с токеном

## Поток аутентификации

1. **Зарегистрируйте пользователя** (POST `/api/users/`) - Аутентификация не требуется
2. **Войдите в систему** (POST `/api/token/`) - Предоставляет токены доступа и обновления
3. **Используйте токен доступа** для всех других API запросов
4. **Обновите токен** (POST `/api/token/refresh/`) при истечении срока действия 