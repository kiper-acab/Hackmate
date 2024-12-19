

## 🚀 Инструкция по запуску

### Клонирование репозитория
Клонируйте проект с помощью команды:
```bash
git clone https://gitlab.crja72.ru/django/2024/autumn/course/projects/team-5.git
```

### Создание виртуальной среды
#### Windows
```cmd
python -m venv venv
```
#### Linux
```bash
sudo apt install python3-venv
python3 -m venv venv
```

### Активация окружения
#### Windows
```cmd
venv\Scripts\activate
```
#### Linux
```bash
source ./venv/bin/activate
```

### Установка зависимостей
- Для продакшн-окружения:
  ```bash
  pip install -r requirements/prod.txt
  ```
- Для разработки:
  ```bash
  pip install -r requirements/dev.txt
  ```
- Для тестирования:
  ```bash
  pip install -r requirements/test.txt
  ```

### Настройка переменных окружения
Перенесите переменные из `.env.template` в `.env`:
```bash
dump-env --template=.env.template --prefix='SECRET_ENV_' > .env
```

### Запуск приложения
Перейдите в каталог `hackmate` и выполните:
```bash
cd hackmate
python manage.py runserver
```

---

## 📊 Миграции базы данных
Проект использует систему миграций для управления изменениями структуры базы данных.

- Создание миграции:
  ```bash
  python manage.py makemigrations
  ```
- Применение миграции:
  ```bash
  python manage.py migrate
  ```

---

## 📦 Фикстуры
Фикстуры помогают загружать и выгружать данные базы данных.

- Загрузка фикстур:
  ```bash
  python manage.py loaddata fixtures/data.json
  ```
- Выгрузка фикстур:
  ```bash
  python -X utf8 manage.py dumpdata --indent 2 catalog > fixtures/data.json
  ```

---

## 📐 ER-диаграмма
![ER-диаграмма](../ER.jpg)
---

## 🌐 Интернационализация
Этот проект поддерживает интернационализацию.

### Создание собственной локализации
1. Добавьте язык в `settings.py`:
   ```python
   LANGUAGES = [
       ("ru", django.utils.translation.gettext_lazy("Русский")),
       ("en", django.utils.translation.gettext_lazy("English")),
       ("lang", django.utils.translation.gettext_lazy("Your_language")),
   ]
   ```
2. Создайте конфигурацию локализации:
   ```bash
   django-admin makemessages -l your_lang
   ```
3. Заполните содержимое файла локализации.
4. Компилируйте переводы:
   ```bash
   django-admin compilemessages
   ```

Подробнее о локализации можно прочитать [здесь](https://habr.com/ru/companies/ruvds/articles/498452/).

---
## ✅ Тестирование
1. Перейдите в каталог `hackmate`:
   ```bash
   cd hackmate
   ```
2. Запустите тесты:
   ```bash
   python manage.py test
   ```
