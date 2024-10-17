import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


def api_request(url, params):
    """Handles API requests and returns the JSON data or raises an error if needed"""
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def shorten_link(token, url):
    params = {
        "access_token": token,
        "url": url,
        "private": 0,
        "v": "5.199"
    }
    response = api_request(
        "https://api.vk.com/method/utils.getShortLink", params)
    return response.get('response', {}).get('short_url')


def count_clicks(token, link_key):
    params = {
        "access_token": token,
        "key": link_key,
        "interval": "forever",
        "v": "5.199"
    }
    response = api_request(
        "https://api.vk.com/method/utils.getLinkStats", params)
    stats = response.get('response', {}).get('stats', [])
    return sum(stat.get('views', 0) for stat in stats)


def is_shortened_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "vk.cc" and parsed_url.path


def process_link(url, token):
    """Processes the URL: if shortened, returns click count; if not, returns shortened link"""
    if is_shortened_link(url):
        link_key = urlparse(url).path[1:]
        return 'clicks', count_clicks(token, link_key)
    return 'short_url', shorten_link(token, url)


def display_result(link_type, proccessed_link):
    if link_type == 'clicks':
        print(f"Общее количество кликов по ссылке: {proccessed_link}")
    elif link_type == 'short_url':
        if proccessed_link:
            print(f"Сокращенная ссылка: {proccessed_link}")
        else:
            print("Error. Please enter a valid link")


def main():
    load_dotenv(".env")
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        raise EnvironmentError(
            "There's no such token in the '.env'. Please,write a valid one")

    url = input("Введите ссылку: ")
    try:
        link_type, proccessed_link = process_link(url, access_token)
        display_result(link_type, proccessed_link)
    except requests.exceptions.HTTPError:
        print("HTTP error: Please check that you entered a token or a link correctly.")


if __name__ == "__main__":
    main()
