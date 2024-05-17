import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta


class TrendyolShop:
    exchange_url = "https://www.tgju.org/profile/price_try"

    last_exchange_rate = None
    last_update_time = None

    def exchange_rates(self):
        # اگر نرخ تبدیل هنوز بازیابی نشده یا بیش از یک روز از آخرین به‌روزرسانی گذشته است
        if not self.last_exchange_rate or (datetime.now() - self.last_update_time) > timedelta(days=1):
            try:
                response = requests.get(self.exchange_url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # پیدا کردن نرخ تبدیل
                tl_rial = soup.find_all(class_="text-left")
                tl_rial_int = int(tl_rial[2].text.replace(",", ""))
                self.last_exchange_rate = tl_rial_int / 10 + 100
                self.last_update_time = datetime.now()
            except Exception as e:
                print(e)
                return 'Call to admin'

        return self.last_exchange_rate

    @staticmethod
    def check_trendyol_url(url):
        regex = re.compile(r'^(https://)(?:www.trendyol.com|ty.gl)(/((?:[\w?!@#$%^&*()+|~><:;{}\][\=&-]*)(?<!/)))+/?', re.IGNORECASE)
        return re.match(regex, url) is not None and re.match(regex, url).group() == url

    @staticmethod
    def fetch_product_data(url):
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

            # Extract other details
            details_elements = soup.find_all(class_="detail-attr-container")
            details = None
            if len(details_elements) > 0:
                details = [i.text for i in details_elements]
                details = details[0].split('\n')

            # Extract selected size
            _size = soup.select_one(".pr-in-sz-pk span span")

            size_element = soup.select_one(".selected") if _size is None else _size
            so_sizes = [size.text for size in soup.find_all(class_="so sp-itm")]
            size = f'out of stock selected size' if size_element is None and so_sizes else (size_element.text if size_element else None)

            # Calculate price in IR
            rate = self.exchange_rates()
            price_ir = int(round(round(price_tl, 1) * rate * 1.28, -3)) if price_tl and rate != 'Call to admin' else None

            #  Extract selected colore
            # todo

            return {
                'price': price_tl,
                'size': size,
                'priceIr': price_ir,
                'rate': rate,
                'imageUrl': image_url,
                'details': details,
            }
        except Exception as e:
            print(e)
            return False

# استفاده از کلاس
# url5 = "https://www.trendyol.com/karaca/linda-pembe-yemek-bicagi-p-35138783?boutiqueId=61&merchantId=253958"
# url4 = "https://www.trendyol.com/karaca/rory-servis-tabagi-19-cm-p-646091822?boutiqueId=61&merchantId=253958"
# url3 = "https://www.trendyol.com/bikelife/kadin-haki-yuksek-bel-genis-paca-kargo-pantolon-p-348872155?merchantId=470862&boutiqueId=61&v=36"
# url1 = "https://www.trendyol.com/bikelife/kadin-haki-yuksek-bel-genis-paca-kargo-pantolon-p-348872155?merchantId=470862&boutiqueId=61&v=34"
# url2 = 'https://www.trendyol.com/betilina/beyaz-vintage-baskili-t-shirt-p-799489054?boutiqueId=61&merchantId=837448&sav=true'
# shop = TrendyolShop()
# url = 'https://www.trendyol.com/betilina/freedom-hypemode-vintage-baskili-t-shirt-p-824604032?merchantId=837448&boutiqueId=61&v=s-m'
# result = shop.extract_data(url1)
# print(result)
