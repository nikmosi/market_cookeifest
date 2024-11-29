# market_cookeifest

# Backend API Documentation

## Эндпоинты

### 1. Получение информации о товаре

**URL:** `/api/products/{product_id}`  
**Метод:** `GET`  
**Описание:** Возвращает информацию о конкретном товаре на основе его идентификатора.

#### Параметры запроса:

- `product_id` (path): Идентификатор товара (обязательный).

#### Пример запроса:

```http
GET /api/products/12345
```

#### Пример ответа:

```javascript
{
  "id": "12345"
  "name": "Название товара",
  "description": "Описание товара",
  "price": 1000.50,
  "delivery": "21.11.2024"
  "rating": 4.5,
  "reviews_count": 120,
  "options": {
    "option1": "value",
    "option2": "value",
    "option3": "value",
  }

  "images": [
    "https://example.com/images/product1.jpg",
    "https://example.com/images/product2.jpg"
  ]
}
```

### 2. Получение аналогичных товаров

**URL:** `/api/products/{product_id}/similar`  
**Метод:** `GET`  
**Описание:** Возвращает список идентификаторов товаров, схожих с указанным товаром.

#### Параметры запроса:

- `product_id` (path): Идентификатор товара (обязательный).

#### Пример запроса:

```http
GET /api/products/12345/similar
```

#### Пример ответа:

```javascript
[54321, 67890, 98765];
```
