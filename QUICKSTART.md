# 🚀 Быстрый старт с API документацией

## 📦 Что было создано

1. **swagger.json** - OpenAPI 3.0 спецификация API
2. **swagger-ui.html** - Интерактивная документация с киберпанк дизайном
3. **API-README.md** - Полное руководство по API
4. **PyPath_API.postman_collection.json** - Postman коллекция всех запросов
5. **PyPath_Dev.postman_environment.json** - Environment для Postman
6. **start-api.bat / start-api.sh** - Скрипты для запуска серверов

## ⚡ Быстрый запуск

### Вариант 1: Автоматический запуск (рекомендуется)

**Windows:**
```bash
start-api.bat
```

**Linux/Mac:**
```bash
chmod +x start-api.sh
./start-api.sh
```

Это запустит:
- Mock API на http://localhost:3000
- Swagger UI на http://localhost:8080/swagger-ui.html

### Вариант 2: Ручной запуск

**Шаг 1 - Установите json-server:**
```bash
npm install -g json-server
```

**Шаг 2 - Запустите Mock API:**
```bash
json-server --watch db.json --port 3000
```

**Шаг 3 - Запустите HTTP сервер для Swagger UI:**
```bash
# Python
python -m http.server 8080

# Или Node.js
npx http-server -p 8080
```

**Шаг 4 - Откройте в браузере:**
```
http://localhost:8080/swagger-ui.html
```

## 📚 Использование документации

### Swagger UI
- Откройте `swagger-ui.html` в браузере
- Все эндпоинты сгруппированы по категориям
- Можно тестировать запросы прямо в браузере (кнопка "Try it out")

### Postman
1. Импортируйте `PyPath_API.postman_collection.json`
2. Импортируйте `PyPath_Dev.postman_environment.json`
3. Выберите environment "PyPath Development"
4. Готово! Все запросы настроены и готовы к использованию

## 🔍 Основные эндпоинты

```
GET    /currentUser          # Информация о пользователе
GET    /stats                # Статистика
GET    /courses              # Список курсов
GET    /leaderboard          # Таблица лидеров
GET    /achievements         # Достижения
GET    /posts                # Посты сообщества
POST   /posts                # Создать пост
GET    /missions             # Миссии
POST   /missions/{id}/submit # Отправить решение
```

## 📖 Примеры запросов

### cURL
```bash
# Получить текущего пользователя
curl http://localhost:3000/currentUser

# Получить достижения по категории
curl http://localhost:3000/achievements?category=coding

# Создать пост
curl -X POST http://localhost:3000/posts \
  -H "Content-Type: application/json" \
  -d '{"content": "Мой пост", "tags": ["Python"]}'
```

### JavaScript
```javascript
// Получить курсы
const response = await fetch('http://localhost:3000/courses');
const courses = await response.json();
console.log(courses);
```

### Python
```python
import requests

# Получить таблицу лидеров
r = requests.get('http://localhost:3000/leaderboard')
print(r.json())
```

## 🎨 Особенности

✅ Полная OpenAPI 3.0 спецификация
✅ 30+ задокументированных эндпоинтов  
✅ Интерактивная документация с киберпанк дизайном
✅ Готовая Postman коллекция
✅ Примеры запросов и ответов
✅ Mock API сервер через JSON Server
✅ Скрипты автозапуска для всех ОС

## 🛠️ Остановка серверов

**Windows:** Просто закройте окна терминала

**Linux/Mac:**
```bash
chmod +x stop-api.sh
./stop-api.sh
```

Или найдите процессы вручную:
```bash
# Найти процессы
lsof -ti:3000    # API Server
lsof -ti:8080    # Swagger UI

# Остановить
kill $(lsof -ti:3000)
kill $(lsof -ti:8080)
```

## 📝 Редактирование документации

1. Отредактируйте `swagger.json`
2. Проверьте на https://editor.swagger.io/
3. Перезагрузите `swagger-ui.html` в браузере

## 🐛 Частые проблемы

**Порт занят:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <номер_процесса> /F

# Linux/Mac
lsof -ti:3000 | xargs kill
```

**json-server не найден:**
```bash
npm install -g json-server
```

**CORS ошибки:**
JSON Server автоматически поддерживает CORS, но если возникают проблемы:
```bash
json-server --watch db.json --port 3000 --middlewares ./cors-middleware.js
```

## 📞 Поддержка

- 📖 Полная документация: `API-README.md`
- 🌐 Swagger UI: http://localhost:8080/swagger-ui.html
- 🔌 Mock API: http://localhost:3000

## 🎉 Готово!

Документация полностью настроена и готова к использованию. Приятной разработки! 🚀
