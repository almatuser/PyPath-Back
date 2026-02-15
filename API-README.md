# 📚 PyPath API Documentation

Swagger документация для PyPath - геймифицированной платформы обучения программированию на Python.

## 🚀 Быстрый старт

### Просмотр документации

1. **Онлайн версия (рекомендуется)**:
   - Откройте файл `swagger-ui.html` в браузере
   - Или запустите локальный сервер (см. ниже)

2. **Через Swagger Editor**:
   - Перейдите на https://editor.swagger.io/
   - Скопируйте содержимое `swagger.json` в редактор

### Запуск локального сервера документации

```bash
# С помощью Python
python -m http.server 8080

# С помощью Node.js (если установлен http-server)
npx http-server -p 8080

# С помощью PHP
php -S localhost:8080
```

Затем откройте в браузере: http://localhost:8080/swagger-ui.html

## 📖 Структура API

### Основные группы эндпоинтов:

#### 👤 Users
- `GET /currentUser` - Получить текущего пользователя
- `PUT /currentUser` - Обновить профиль
- `GET /stats` - Статистика пользователя
- `GET /activity` - Активность по дням
- `GET /skills` - Навыки пользователя

#### 🎓 Courses
- `GET /courses` - Список всех курсов
- `GET /courses/{id}` - Детали курса

#### 🏆 Achievements
- `GET /achievements` - Все достижения с прогрессом
- Фильтры: по категории (coding, community, streak, secret)

#### 📊 Leaderboard
- `GET /leaderboard` - Таблица лидеров
- Параметры: scope (global/friends/school), period (all/month)

#### 💬 Community
- `GET /posts` - Посты сообщества
- `POST /posts` - Создать новый пост
- `POST /posts/{id}/like` - Лайкнуть пост
- `GET /friends` - Список друзей

#### 🎮 Missions
- `GET /missions` - Список миссий
- `GET /missions/{id}` - Детали миссии
- `POST /missions/{id}/submit` - Отправить решение

#### ⚙️ System
- `GET /uiData` - Конфигурация UI
- `GET /logs` - Системные логи

## 🔐 Аутентификация

API поддерживает два метода аутентификации:

1. **Bearer Token (JWT)**:
```bash
Authorization: Bearer <your_jwt_token>
```

2. **API Key**:
```bash
X-API-Key: <your_api_key>
```

## 🧪 Тестирование API

### С помощью JSON Server (Mock API)

Установите JSON Server:
```bash
npm install -g json-server
```

Запустите mock API:
```bash
json-server --watch db.json --port 3000
```

API будет доступен по адресу: http://localhost:3000

### Примеры запросов

#### cURL
```bash
# Получить текущего пользователя
curl http://localhost:3000/currentUser

# Получить курсы
curl http://localhost:3000/courses

# Создать пост
curl -X POST http://localhost:3000/posts \
  -H "Content-Type: application/json" \
  -d '{"content": "Мой первый пост", "tags": ["Python", "Beginners"]}'
```

#### JavaScript (Fetch)
```javascript
// Получить достижения
fetch('http://localhost:3000/achievements')
  .then(res => res.json())
  .then(data => console.log(data));

// Обновить профиль
fetch('http://localhost:3000/currentUser', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    bio: 'Новая биография',
    settings: {
      theme: 'dark',
      notifications: true
    }
  })
});
```

#### Python (Requests)
```python
import requests

# Получить таблицу лидеров
response = requests.get('http://localhost:3000/leaderboard')
leaderboard = response.json()
print(leaderboard)

# Лайкнуть пост
requests.post('http://localhost:3000/posts/1/like')
```

## 📊 Модели данных

### User
Основная модель пользователя с профилем, уровнем, XP и настройками.

### Achievement
Система достижений с 4 уровнями редкости:
- `common` - Обычный
- `rare` - Редкий
- `epic` - Эпический
- `legendary` - Легендарный

### Course
Игровые главы с прогрессом, сложностью и БОСС-уровнями.

### Mission
Интерактивные задания с файлами кода, целями и теорией.

## 🎨 Особенности

- ✅ Полная типизация схем данных
- ✅ Подробные описания всех эндпоинтов
- ✅ Примеры запросов и ответов
- ✅ Группировка по тегам
- ✅ Поддержка фильтрации и пагинации
- ✅ JWT и API Key аутентификация
- ✅ Киберпанк стилизация UI

## 🛠️ Разработка

### Обновление документации

1. Отредактируйте `swagger.json`
2. Проверьте валидность на https://validator.swagger.io/
3. Обновите версию в `info.version`
4. Перезагрузите `swagger-ui.html` в браузере

### Генерация клиента

Используйте Swagger Codegen для генерации клиентских библиотек:

```bash
# Для JavaScript/TypeScript
npx @openapitools/openapi-generator-cli generate \
  -i swagger.json \
  -g typescript-fetch \
  -o ./generated/client

# Для Python
npx @openapitools/openapi-generator-cli generate \
  -i swagger.json \
  -g python \
  -o ./generated/python-client
```

## 📝 Конвенции API

- Все эндпоинты возвращают JSON
- Даты в формате ISO 8601
- Пагинация через query параметры `?page=1&limit=20`
- Ошибки следуют RFC 7807 (Problem Details)
- HTTP коды:
  - `200` - Успех
  - `201` - Создано
  - `400` - Неверный запрос
  - `401` - Не авторизован
  - `404` - Не найдено
  - `500` - Ошибка сервера

## 🌐 Полезные ссылки

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [JSON Server Documentation](https://github.com/typicode/json-server)
- [Swagger Editor](https://editor.swagger.io/)

## 📄 Лицензия

MIT License

## 🤝 Поддержка

Если у вас возникли вопросы или предложения:
- Email: support@pypath.com
- GitHub: [Issues](https://github.com/pypath/api/issues)

---

**Made with 💙 for Code Arcade Community**
