# API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication
Currently, the API does not require authentication. This should be implemented in a production environment.

## Endpoints

### Users

#### List Users
```http
GET /api/users/
```
Response:
```json
[
    {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "weight": 75.5,
        "height": 180.0,
        "age": 30,
        "diet_type_id": 1
    }
]
```

#### Create User
```http
POST /api/users/
```
Request:
```json
{
    "username": "jane_doe",
    "password": "secure123",
    "email": "jane@example.com",
    "weight": 65.0,
    "height": 165.0,
    "age": 25,
    "diet_type_id": 2
}
```

#### Get User
```http
GET /api/users/{id}/
```

#### Update User
```http
PATCH /api/users/{id}/
```
Request:
```json
{
    "weight": 70.0,
    "height": 170.0
}
```

#### Delete User
```http
DELETE /api/users/{id}/
```

#### Verify Password
```http
POST /api/users/{id}/verify_password/
```
Request:
```json
{
    "password": "secure123"
}
```
Response:
```json
{
    "is_valid": true
}
```

### Meal Plans

#### List Meal Plans
```http
GET /api/meal-plans/
```
Response:
```json
[
    {
        "id": 1,
        "user_id": 1,
        "duration": 14,
        "total_price": 1000.0
    }
]
```

#### Create Meal Plan
```http
POST /api/meal-plans/
```
Request:
```json
{
    "user_id": 1,
    "duration": 30,
    "total_price": 2000.0
}
```

#### Get Meal Plan
```http
GET /api/meal-plans/{id}/
```

#### Delete Meal Plan
```http
DELETE /api/meal-plans/{id}/
```

#### Calculate Plan Price
```http
GET /api/meal-plans/{id}/calculate_price/
```
Response:
```json
{
    "price": 1000.0
}
```

### Meals

#### List Meals
```http
GET /api/meals/
```
Response:
```json
[
    {
        "id": 1,
        "name": "Салат Цезарь",
        "description": "Классический салат с курицей и сухариками",
        "price": 15.99,
        "diet_type_id": 1
    }
]
```

#### Create Meal
```http
POST /api/meals/
```
Request:
```json
{
    "name": "Греческий салат",
    "description": "Свежий салат с овощами и сыром фета",
    "price": 12.99,
    "diet_type_id": 1
}
```

#### Get Meal
```http
GET /api/meals/{id}/
```

#### Delete Meal
```http
DELETE /api/meals/{id}/
```

#### Calculate Meal Price
```http
GET /api/meals/{id}/calculate_price/
```
Response:
```json
{
    "price": 12.99
}
```

### Ingredients

#### List Ingredients
```http
GET /api/ingredients/
```
Response:
```json
[
    {
        "id": 1,
        "name": "Куриная грудка",
        "price_per_unit": 5.99,
        "unit": "кг",
        "store_name": "Ашан",
        "valid_from": "2024-01-01T00:00:00Z"
    }
]
```

#### Create Ingredient
```http
POST /api/ingredients/
```
Request:
```json
{
    "name": "Оливковое масло",
    "price_per_unit": 8.99,
    "unit": "л",
    "store_name": "Магнит",
    "valid_from": "2024-01-01T00:00:00Z"
}
```

#### Get Ingredient
```http
GET /api/ingredients/{id}/
```

#### Delete Ingredient
```http
DELETE /api/ingredients/{id}/
```

### Diet Types

#### List Diet Types
```http
GET /api/diet-types/
```
Response:
```json
[
    {
        "id": 1,
        "name": "Средиземноморская",
        "description": "Диета, основанная на традиционной кухне стран Средиземноморья",
        "is_restricted": false
    }
]
```

#### Create Diet Type
```http
POST /api/diet-types/
```
Request:
```json
{
    "name": "Кето",
    "description": "Низкоуглеводная диета с высоким содержанием жиров",
    "is_restricted": true
}
```

#### Get Diet Type
```http
GET /api/diet-types/{id}/
```

#### Delete Diet Type
```http
DELETE /api/diet-types/{id}/
```

### Favorites

#### List Favorites
```http
GET /api/favorites/
```
Response:
```json
[
    {
        "id": 1,
        "user_id": 1,
        "meal_id": 1
    }
]
```

#### Create Favorite
```http
POST /api/favorites/
```
Request:
```json
{
    "user_id": 1,
    "meal_id": 2
}
```

#### Get Favorite
```http
GET /api/favorites/{id}/
```

#### Delete Favorite
```http
DELETE /api/favorites/{id}/
```

## Testing with Postman

1. Import the following collection into Postman:
```json
{
    "info": {
        "name": "Meal Planning API",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Users",
            "item": [
                {
                    "name": "List Users",
                    "request": {
                        "method": "GET",
                        "url": "http://localhost:8000/api/users/"
                    }
                },
                {
                    "name": "Create User",
                    "request": {
                        "method": "POST",
                        "url": "http://localhost:8000/api/users/",
                        "body": {
                            "mode": "raw",
                            "raw": "{\n    \"username\": \"test_user\",\n    \"password\": \"test123\",\n    \"email\": \"test@example.com\",\n    \"weight\": 70.0,\n    \"height\": 175.0,\n    \"age\": 25,\n    \"diet_type_id\": 1\n}",
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

2. Create similar collections for other endpoints (Meal Plans, Meals, Ingredients, Diet Types, Favorites)

## Testing with Curl

### Users

#### List Users
```bash
curl -X GET http://localhost:8000/api/users/
```

#### Create User
```bash
curl -X POST http://localhost:8000/api/users/ \
    -H "Content-Type: application/json" \
    -d '{
        "username": "test_user",
        "password": "test123",
        "email": "test@example.com",
        "weight": 70.0,
        "height": 175.0,
        "age": 25,
        "diet_type_id": 1
    }'
```

#### Get User
```bash
curl -X GET http://localhost:8000/api/users/1/
```

#### Update User
```bash
curl -X PATCH http://localhost:8000/api/users/1/ \
    -H "Content-Type: application/json" \
    -d '{
        "weight": 75.0,
        "height": 180.0
    }'
```

#### Delete User
```bash
curl -X DELETE http://localhost:8000/api/users/1/
```

#### Verify Password
```bash
curl -X POST http://localhost:8000/api/users/1/verify_password/ \
    -H "Content-Type: application/json" \
    -d '{
        "password": "test123"
    }'
```

Create similar curl commands for other endpoints following the same pattern. 