import requests
import time
from bs4 import BeautifulSoup

page_url = 'https://shop.adidas.jp/men/'


def men_category():
    resp = requests.get(page_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    elements = soup.find_all('a', class_='lpc-teaserCarousel_link')
    # print(elements)
    href_list = [element['href'] for element in elements]
    return href_list


def items(category):
    params = category.split('?')[-1] + '&limit=40'
    url = 'https://shop.adidas.jp/f/v1/pub/product/list?' + params
    resp = requests.get(url)
    if not resp.ok:
        return {}
    resp = resp.json()
    list_of_items = resp['articles_sort_list']
    print(list_of_items)
    print(len(list_of_items))
    time.sleep(2)
    # print(params)



def main():
    categories = men_category()
    for category in categories:
        items(category)


main()


# var = men_category()
# for i in var:
#     print(i)

# r = requests.get(page_url)
# print(r.status_code)