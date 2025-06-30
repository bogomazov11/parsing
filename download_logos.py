# Сохраняет картинки по ссылке (с прокси)
import os
import re
import urllib.request
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

doc_numbers = ['NUMBERS']


import time
import random
os.environ['HTTP_PROXY'] = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
os.environ['HTTPS_PROXY'] = os.environ['HTTP_PROXY']

HEADERS = {'User-Agent': 'Mozilla/5.0'}


def download_tm_logo(doc_number: int):
    """
    Скачивает изображение товарного знака (без суффикса -m) по номеру документа.
    Имя файла формируется из номера документа + оригинального расширения.
    """
    time.sleep(random.uniform(1, 4))
    page_url = f"http://www1.fips.ru/fips_servl/fips_servlet?DB=RUTM&DocNumber={doc_number}"
    req = urllib.request.Request(page_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read()

    soup = BeautifulSoup(html, 'html.parser')
    img_tag = soup.find('img', src=lambda s: s and '-m.' in s)
    if not img_tag:
        print('Мини-изображение не найдено')
        return

    anchor = img_tag.find_parent('a', href=True)
    if not anchor:
        print('Ссылка на полное изображение не найдена')
        return

    img_url = anchor['href']
    if not img_url.startswith(('http://', 'https://')):
        img_url = urljoin(page_url, img_url)

    img_req = urllib.request.Request(img_url, headers=HEADERS)
    with urllib.request.urlopen(img_req, timeout=30) as img_resp:
        data = img_resp.read()

    ext = os.path.splitext(urlparse(img_url).path)[1]
    filename = f"{doc_number}{ext}"
    os.makedirs('logo', exist_ok=True)
    filepath = os.path.join('logo', filename)
    with open(filepath, 'wb') as f:
        f.write(data)

    print(f"Изображение сохранено: {filepath}")


if __name__ == '__main__':
    for i in doc_numbers:
        print(i)
        download_tm_logo(i)

