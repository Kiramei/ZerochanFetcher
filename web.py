HOST_URL = 'https://www.zerochan.net/Tendou+Alice'
HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

import requests


def get_page(url):
    response = requests.get(url, headers=HEADERS)
    return response.text


def get_page_num(page):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page, 'html.parser')
    # 找到class为pagination的div标签
    pagination = soup.find('nav', class_='pagination')
    # 找到其中的span标签，得到其中的文本 page 1 of 19
    txt = pagination.find_all('span')[-1].text
    # 用空格分割文本，得到['page', '1', 'of', '19']
    txt = txt.split()
    # 返回倒数第一个元素
    return int(txt[-1])


def get_image_urls(page):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page, 'html.parser')
    images = soup.find_all('a')
    img_list = []
    for image in images:
        if 'href' in list(image.attrs.keys()) and '.full.' in image['href']:
            img_list.append(image['href'])
    return img_list


def download_image(url, path):
    response = requests.get(url, headers=HEADERS)
    with open(path, 'wb') as file:
        file.write(response.content)
    print(f'Downloaded {path}')


def main():
    print('Tentou Alice Fetcher v1.0')
    pages = []
    page = get_page(HOST_URL)
    pages.append(page)
    image_urls = []

    page_nums = get_page_num(page)
    print(f'Total Pages: {page_nums}')

    def _get_page(page_num):
        _page = get_page(f'{HOST_URL}?p={page_num}')
        pages.append(_page)

    for i in range(1, page_nums + 1):
        import threading
        threading.Thread(target=_get_page, args=(i, )).start()

    print('Downloading Page Info...')

    while len(pages) < page_nums:
        import time
        time.sleep(1)

    print('Downloaded Page Info')

    print('Getting Image URLs...')

    def _get_image_urls(page):
        image_urls.extend(get_image_urls(page))

    threads = []
    for page in pages:
        t = threading.Thread(target=_get_image_urls, args=(page, ))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    image_urls = list(set(image_urls))
    print('Image Amount:', len(image_urls))

    print('Start Downloading Images...')
    import os
    if not os.path.exists('images'):
        os.mkdir('images')

    threads_num = 50

    for i, url in enumerate(image_urls):
        import threading
        while True:
            if threading.active_count() < threads_num:
                break
            else:
                import time
                time.sleep(.5)
        threading.Thread(target=download_image,
                         args=(url, f'images/{i}.png')).start()
    
    print('All Tentou Alice Images Downloaded! Have Fun!')

if __name__ == '__main__':
    main()
