```markdown
# Сокращение ссылок и счетчик кликов

Этот скрипт позволяет сокращать ссылки с помощью VK API и отслеживать общее количество кликов по коротким ссылкам. Отличное решение для создания коротких ссылок и контроля их популярности!

## Возможности

- **Сокращение ссылок**: Преобразует длинные ссылки в короткие ссылки `vk.cc`.
- **Отслеживание кликов**: Узнает общее количество кликов по короткой ссылке.
- **Работа с HTTP и HTTPS**: Принимает как HTTP, так и HTTPS ссылки.
- **Надежность**: Обрабатывает ошибки API и сети с помощью описательных сообщений.
- **Удобство использования**: Поддерживает передачу ссылок через командную строку, что упрощает работу с несколькими ссылками.

## Требования

- **Python 3.x**
- **Библиотека Requests**: Установите с помощью `pip install requests`
- **Библиотека python-dotenv**: Установите с помощью `pip install python-dotenv`
- **VK API токен**: Сохраните токен в файле `.env`

## Настройка

1. Склонируйте этот репозиторий на ваш компьютер.
2. Создайте файл `.env` в той же директории, что и скрипт. В этом файле добавьте VK API токен:
   ```plaintext
   ACCESS_TOKEN=ваш_токен_vk
   ```
   Замените `ваш_токен_vk` на ваш реальный токен VK API.

## Использование

1. **Запустите скрипт**:
   ```bash
   python3 main.py <url>
   ```
   Замените `<url>` на ссылку, которую вы хотите сократить или проверить.
   
2. **Пример использования**:
   - **Чтобы сократить ссылку**, выполните:
     ```bash
     python3 main.py https://www.example.com
     ```
     Скрипт вернет короткую ссылку `vk.cc`:
     ```plaintext
     Сокращенная ссылка: https://vk.cc/xxxxxx
     ```
   - **Чтобы проверить количество кликов для сокращенной ссылки**, выполните:
     ```bash
     python3 main.py https://vk.cc/xxxxxx
     ```
     Скрипт вернет общее количество кликов:
     ```plaintext
     Общее количество кликов по ссылке: 42
     ```

## Функции

### `shorten_link(token, url)`

Отправляет запрос к VK API для сокращения ссылки. Возвращает короткую ссылку при успешном запросе или сообщение об ошибке.

### `count_clicks(token, link_key)`

Получает общее количество кликов по ссылке `vk.cc` с помощью VK API. Возвращает число кликов или сообщение об ошибке при сбое.

### `is_shortened_link(url)`

Проверяет, является ли ссылка `vk.cc`. Если да, вызывает `count_clicks`, иначе вызывает `shorten_link`. Возвращает общее количество кликов для коротких ссылок или новую короткую ссылку для длинных URL.

### `main()`

Обрабатывает ввод пользователя через командную строку и выводит результат (либо количество кликов, либо короткую ссылку).

