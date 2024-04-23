import requests
import time
from bs4 import BeautifulSoup

page_url = 'https://shop.adidas.jp/men/'


def get_details(content, tag, selector):
    try:
        soup = BeautifulSoup(content.text, 'html.parser')
        text = soup.find(tag, class_=selector)
        return text.text
    except Exception:
        return ""


def get_available_size(content, tag, selector):
    try:
        soup = BeautifulSoup(content.text, 'html.parser')
        size = soup.find(tag, class_=selector)
        all_sizes = ' '.join(size.stripped_strings)
        return all_sizes
    except Exception:
        return ""


def get_breadcrumbs(content, tag, selector):
    try:
        soup = BeautifulSoup(content.text, 'html.parser')
        bread = soup.find(tag, class_=selector)
        breadcrumbs = [item.text.strip() for item in bread.find_all("li")]
        return ' '.join(breadcrumbs)
    except Exception:
        return ""


def get_sense(content, tag, selector):
    try:
        soup = BeautifulSoup(content.text, 'html.parser')
        sense = soup.find(tag, class_=selector)
        if not sense:
            return None
        else:
            sense = sense.get('class')
        record = 0
        for sc in sense:
            if sc.startswith('mod-marker_'):
                record = sc.strip('mod-marker_').replace('_', '.')
                break
        return record
    except Exception:
        return ""


def men_category():
    resp = requests.get(page_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    elements = soup.find_all('a', class_='lpc-teaserCarousel_link')
    href_list = [element['href'] for element in elements]
    return href_list


def product_details(product_urls):
    for product_url in product_urls:
        time.sleep(0.3)
        content = requests.get(product_url)
        details = {
            'url': product_url,
            'breadcrumb': get_breadcrumbs(content, 'ul', 'breadcrumbList'),
            'category': get_details(content, 'a', 'groupName'),
            'product_name': get_details(content, 'h1', 'itemTitle'),
            'price': get_details(content, 'span', 'price-value'),
            'available_sizes': get_available_size(content, 'ul', 'sizeSelectorList'),
            'sense': get_sense(content, 'span', 'test-marker'),
            'title_description': get_details(content, 'h4', 'itemFeature'),
            'general_description': get_details(content, 'div', 'commentItem-mainText'),
        }
        print(details)
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
