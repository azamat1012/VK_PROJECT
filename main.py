import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

CURRENT_PATH = os.path.dirname(__file__)
load_dotenv(f"{CURRENT_PATH}/secrets.env")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def shorten_link(token, url):
    params = {
        "access_token": token,
        "url": url,
        "private": 0,
        "v": "5.199"
    }
    try:
        response = requests.get(
            "https://api.vk.com/method/utils.getShortLink", params=params)
        response.raise_for_status()
        data = response.json()
        if 'response' in data:
            return data['response']['short_url']
        else:
            return "Ошибка сети: Пожалуйста, введите актуальную ссылку."
    except requests.exceptions.RequestException as e:
        return f"Ошибка сети: {e}"


def count_clicks(token, link_key):
    params = {
        "access_token": token,
        "key": link_key,
        "interval": "forever",
        "v": "5.199"
    }
    try:
        response = requests.get(
            "https://api.vk.com/method/utils.getLinkStats", params=params)
        response.raise_for_status()
        data = response.json()
        if 'response' in data:
            total_clicks = sum(stat['views']
                               for stat in data['response']['stats'])
            return total_clicks
        else:
            return "Ошибка API: Пожалуйста, попробуйте снова."
    except requests.exceptions.RequestException as e:
        return f"Ошибка сети: {e}"


def is_shorten_link(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == "vk.cc" and len(parsed_url.path) <= 7:
        link_key = parsed_url.path[1:]
        return count_clicks(ACCESS_TOKEN, link_key)
    else:
        return shorten_link(ACCESS_TOKEN, url)


def main():
    url = input("Введите ссылку: ")
    try:
        result = is_shorten_link(url)
        if isinstance(result, int):
            print(f"Общее количество кликов по ссылке: {result}")
        else:
            print(f"Сокращенная ссылка: {result}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
