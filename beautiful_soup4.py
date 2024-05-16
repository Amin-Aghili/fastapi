import requests
from bs4 import BeautifulSoup
import re

class TrendyolShop:
    exchange_url = "https://www.tgju.org/profile/price_try"

    def exchange_rates(self):
        try:
            response = requests.get(self.exchange_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # پیدا کردن نرخ تبدیل
            tl_rial = soup.find_all(class_="text-left")
            tl_rial_int = int(tl_rial[2].text.replace(",", ""))
            return tl_rial_int / 10 + 100
        except Exception as e:
            print(e)
            return 'Call to admin'

    def check_trendyol_url(self, url):
        regex = re.compile(r'^(https://)(?:www.trendyol.com|ty.gl)(/((?:[\w?!@#$%^&*()+|~><:;{}\][\=&-]*)(?<!/)))+/?', re.IGNORECASE)
        return re.match(regex, url) is not None and re.match(regex, url).group() == url

    def fetch_product_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return None
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as e:
            print(e)
            return None

    def extract_data(self, url):
        if not self.check_trendyol_url(url):
            return False

        soup = self.fetch_product_data(url)
        if not soup:
            return False

        try:
            # Extract image URL
            
            images = soup.findAll('img')
            image_url = images[1]['src']

            # Extract price
            price_element = soup.select('div.product-price-container span[class^="prc-"]')
            price_tl = float(price_element[-1].text.split()[0].replace('.', '').replace(',', '.')) if price_element else None

            # Extract sizes
            is_size = soup.find_all(class_="variants")
            sizes = False
            if len(is_size) > 0:
                list_size = [i.text for i in soup.find_all(class_="sp-itm")]
                print(list_size)
                so_sizes = [size.text for size in soup.find_all(class_="so sp-itm")]
                sizes = [size for size in list_size if size not in so_sizes]

            # Extract other details
            details_elements = soup.find_all(class_="detail-attr-container")
            details = None
            if len(details_elements) > 0:
                details = [i.text for i in details_elements]
                details = details[0].split('\n')

            # Extract selected size
            size_element = soup.find(class_="size-variant-attr-value")
            so_sizes = [size.text for size in soup.find_all(class_="so sp-itm")]
            size = f'out of stock "{size_element.text}" size' if size_element and size_element.text in so_sizes else (size_element.text if size_element else False)

            # Calculate price in IR
            rate = self.exchange_rates()
            price_ir = int(round(round(price_tl, 1) * rate * 1.28, -3)) if price_tl and rate != 'Call to admin' else None

            return {
                'image_url': image_url,
                'price': price_tl,
                'size': size,
                'sizes': sizes,
                'details': details,
                'priceIr': price_ir,
                'rate': rate
            }
        except Exception as e:
            print(e)
            return False

# # استفاده از کلاس
# shop = TrendyolShop()
# url = 'https://www.trendyol.com/nilu-moda/2-li-kristal-kadin-gozlugu-seti-p-239281625?merchantId=310861'
# result = shop.extract_data(url)
# print(result)
