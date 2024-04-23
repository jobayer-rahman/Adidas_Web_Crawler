import requests
import time
from bs4 import BeautifulSoup

page_url = 'https://shop.adidas.jp/men/'


def get_details(page_url, tag, selector):
    try:
        resp = requests.get(page_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.find(tag, class_=selector)
        return text.text
    except Exception:
        return ""


def get_available_size(page_url, tag, selector):
    try:
        resp = requests.get(page_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        size = soup.find(tag, class_=selector)
        all_sizes = ' '.join(size.stripped_strings)
        return all_sizes
    except Exception:
        return ""


def get_breadcrumbs(page_url, tag, selector):
    try:
        resp = requests.get(page_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        bread = soup.find(tag, class_=selector)
        breadcrumbs = [item.text.strip() for item in bread.find_all("li")]
        return ' '.join(breadcrumbs)
    except Exception:
        return ""


def men_category():
    resp = requests.get(page_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    elements = soup.find_all('a', class_='lpc-teaserCarousel_link')
    # print(elements)
    href_list = [element['href'] for element in elements]
    return href_list


def product_details(product_urls):
    for product_url in product_urls:
        details = {
            'url': product_url,
            'breadcrumb': get_breadcrumbs(product_url, 'ul', 'breadcrumbList'),
            'category': get_details(product_url, 'a', 'groupName'),
            'product_name': get_details(product_url, 'h1', 'itemTitle'),
            'price': get_details(product_url, 'span', 'price-value'),
            'available_sizes': get_available_size(product_url, 'ul', 'sizeSelectorList'),
            'title_description': get_details(product_url, 'h4', 'itemFeature'),
            'general_description': get_details(product_url, 'div', 'commentItem-mainText'),
        }
        print(details)
        # print(product_url)
        # resp = requests.get(product_url)
        # if resp.ok:
        #     print("Success")
        break


def items(category):
    params = category.split('?')[-1] + '&limit=40'
    url = 'https://shop.adidas.jp/f/v1/pub/product/list?' + params
    resp = requests.get(url)
    if not resp.ok:
        return {}
    resp = resp.json()
    list_of_items = resp['articles_sort_list']
    time.sleep(2)
    product_urls = [
        f'https://shop.adidas.jp/products/{item}/' for item in list_of_items
    ]
    print(product_urls)
    return product_details(product_urls)


def main():
    categories = men_category()
    for category in categories:
        items(category)


main()
