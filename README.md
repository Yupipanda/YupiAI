<h1 align="center">YupiAI</h1>

# 👋 Привет, друг!

Меня зовут YupiAI, и я был создан разработчиком [Yupipanda](https://github.com/yupipanda).

## Обо мне

Я использую мощные открытые модели искусственного интеллекта от таких платформ, как [Hugging Face](https://huggingface.co/) и [Mistral AI](https://mistral.ai/), чтобы помогать тебе с различными задачами. Эти модели позволяют мне генерировать текст, анализировать информацию и даже создавать уникальные изображения.

## Что я могу делать?

- **Генерация текста:** Я могу писать статьи, эссе, письма и многое другое.
- **Поиск информации:** Использую DuckDuckGo Search для поиска ответов на твои вопросы прямо в интернете.
- **Создание изображений:** Умею превращать текстовые описания в визуальные образы.
- **Работа с голосом:** Могу преобразовывать голосовые сообщения в текст и наоборот.
- **Анализ документов:** Способен просматривать и анализировать фотографии и PDF-документы.
- **Сокращение текста:** Помогаю сделать длинные тексты короче без потери смысла.

### Важно знать

Некоторые из используемых мной моделей могут использовать данные твоих запросов для дальнейшего обучения. Это помогает улучшать качество моих ответов и расширять мои возможности.

### Для начала работы клонируйте репозиторий самого бота:

```bash
git clone https://github.com/Yupipanda/summarizebot.git
cd summarizebot
```

#### Настройте файл [.env](https://github.com/Yupipanda/YupiAI/blob/master/.env), там и так все понятно.

# Ну а дальше:

## Если Docker:

#### Настройте файл [Dockerfile](https://github.com/Yupipanda/YupiAI/blob/master/Dockerfile)

### Если бот будет работать пулами, то:

```dockerfile
CMD ["poetry", "run", "python3", "main_pol.py"]
```
```bash
sudo docker build -t yupiai .
sudo docker run -d --restart=always --name yupiai-container yupiai
```
### Иначе

#### Если бот будет работать вебхуком с кастомными сертификатами:

```dockerfile
CMD ["poetry", "run", "python3", "main_web.py"]
```

#### Если бот будет работать вебхуком без кастомных сертификатов:

```dockerfile
CMD ["poetry", "run", "python3", "main_web.py"]
```

##### Далее

```bash
sudo docker build -t yupiai .
sudo docker run -d -p <порт, который вы указали в самом файле запуска>:<ну сами поймете> --restart=always --name yupiai-container yupiai
```

## Без Docker:

```bash
pip install poetry
poetry config virtualenvs.in-project true
poetry install
sudo poetry run python3 <имя_нужного_вам_скрипта>.py
```

### Также не забудьте настроить [allowed_users.py](https://github.com/Yupipanda/YupiAI/blob/master/app/utils/allowed_users.py) для доступа пользователей к боту.
