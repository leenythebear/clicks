import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def is_bitlink(bitly_token, url):
    bitlink_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"
    headers = {
        "Authorization": f"Bearer {bitly_token}"
    }
    response = requests.get(bitlink_url, headers=headers)
    return response.ok
    
  
def shorten_link(bitly_token, url):
    bitlink_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        "Authorization": f"Bearer {bitly_token}"
    }
    payload = {"long_url": url}
    response = requests.post(bitlink_url, json=payload, headers=headers)
    response.raise_for_status()
    link = response.json()["link"]
    return link

  
def count_clicks(bitly_token, link):
    params_for_url = {'units': '-1'}
    bitlink_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    headers = {
        "Authorization": f"Bearer {bitly_token}"
    }
    response = requests.get(bitlink_url, headers=headers, params=params_for_url)
    response.raise_for_status()
    return response.json()['total_clicks']


if __name__ == "__main__":
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(description='Сокращение ссылок и подсчет количества переходов по ним')
    parser.add_argument('link', help='Ссылка на сайт')
    args = parser.parse_args()
    url = args.link
    parsed_link = urlparse(url)
    link = ''.join([parsed_link.netloc, parsed_link.path])
    if is_bitlink(bitly_token, link):
        try:
            clicks = count_clicks(bitly_token, link)
            print(clicks)
        except requests.exceptions.HTTPError as error:
            print(f"Во время получения данных о количестве переходов произошла следующая ошибка: {error}")
    else:
        try:
            link = shorten_link(bitly_token, url)
            print(link)
        except requests.exceptions.HTTPError as error:
          print(f"Во время получения короткой ссылки произошла следующая ошибка: {error}")
        