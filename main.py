import os
import requests
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    params = {
        "access_token": token,
        "url": url,
        "private": 0,
        "v": "5.199"
    }
    response = requests.get(
        "https://api.vk.com/method/utils.getShortLink", params)
    response.raise_for_status()
    return response.json().get('response', {}).get('short_url')


def count_clicks(token, link_key):
    params = {
        "access_token": token,
        "key": link_key,
        "interval": "forever",
        "v": "5.199"
    }
    response = requests.get(
        "https://api.vk.com/method/utils.getLinkStats", params)
    response.raise_for_status()
    stats = response.json().get('response', {}).get('stats', [])
    return sum(stat.get('views', 0) for stat in stats)


def is_shortened_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "vk.cc" and parsed_url.path


def main():
    load_dotenv(".env")
    vk_access_token = os.getenv("VK_ACCESS_TOKEN")
    if not vk_access_token:
        raise EnvironmentError(
            "There's no such token in the '.env'. Please,write a valid one")
    parser = argparse.ArgumentParser(
        description="Shorten a URL or get click statistics for a shortened URL.")
    parser.add_argument(
        "url", help="This will  show the  shortenn form of link  you've sent")
    args = parser.parse_args()

    url = args.url
    try:
        if is_shortened_link(url):
            link_key = urlparse(url).path[1:]
            clicks = count_clicks(vk_access_token, link_key)
            print(f"Общее количество кликов по  ссылке: {clicks}")
        else:
            short_url = shorten_link(vk_access_token, url)
            if short_url:
                print(f"Сокращенная ссылка: {short_url}")
            else:
                print("Error. Please enter a valid link")

    except requests.exceptions.HTTPError:
        print("HTTP error: Please check that you entered a token or a link correctly.")


if __name__ == "__main__":
    main()
