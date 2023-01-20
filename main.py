import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def shorten_link(token, link):
    token_headers = {'Authorization': f'Bearer {token}'}
    payload = {"long_url": link}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=token_headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, cut_link):
    token_headers = {'Authorization': f'Bearer {token}'}
    params = (
        ('units', '-1'),
    )
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{cut_link}/clicks/summary',
                            headers=token_headers,
                            params=params)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, cut_link):
    token_headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{cut_link}', headers=token_headers)
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Введите ссылку'
    )
    parser.add_argument('name', help='Ваша ссылка')
    args = parser.parse_args()
    link = args.name
    token = os.getenv("BITLY_TOKEN")
    parsed_link = urlparse(link)
    cut_link = f'{parsed_link.netloc}{parsed_link.path}'
    try:
        if is_bitlink(token, cut_link):
            clicks_count = count_clicks(token, cut_link)
            print('Количество кликов:', clicks_count)
        else:
            bitlink = shorten_link(token, link)
            print('Битлинк', bitlink)
    except requests.exceptions.HTTPError:
        print('Вы ввели неправильную ссылку или неверный токен.')


if __name__ == "__main__":
    main()
