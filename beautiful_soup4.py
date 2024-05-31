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
            return None

        soup = self.fetch_product_data(url)
        if not soup:
            return None

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
            list_items = soup.find_all("li", "detail-attr-item")

            # Iterate through list items to find the one with "Renk"
            color = None
            for li in list_items:
                if 'Renk' in li.text:
                    color = li.text.replace('Renk', '').strip()
                    break

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
                'color': color,
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
# url0 = 'https://www.trendyol.com/kotan/siyah-bagcikli-inci-detayli-kalin-taban-spor-ayakkabi-p-460501577?merchantId=657182&boutiqueId=61&v=39'
# result = shop.extract_data('url0')
# print(result)
#
# # [<div class="product-detail-wrapper"><div class="pr-in-w"><div><div class="pr-in-cn"><div><h1 class="pr-new-br" data-drroot="h1"><a class="product-brand-name-with-link" href="/kotan-x-b158752">KOTAN</a> <span>Beyaz Bağcıklı Inci Detaylı Kalın Taban Spor Ayakkabı</span></h1></div><div class="pr-in-ratings"></div><div class="social-proof-wrapper"><div class="socialProofWrapper" data-testid="social-proof"></div></div><div class="product-price-container"><div class="generic-tooltip right"><div class="featured-price-container clickable" component-id="6"><div class="featured-price-box"><div class="featured-price-info"><div class="featured-price-discount"></div>Son 7 Günün En Düşük Fiyatı!</div><div class="featured-prices"><span class="prc-dsc">627,48 TL</span></div></div></div></div></div><div class="product-info-badges"><div class="installment-placeholder"></div></div></div></div></div><div class="slicing-attribute-placeholder" data-dr-hide="true"></div><div class="size-variant-wrapper size-variant-wrapper--without-expectation" data-drroot="size-variant"><div class="size-variant-title-wrapper"><span class="size-variant-title"><span class="size-variant-title--bold">Beden</span>: <span class="size-variant-attr-value">38</span></span></div><div class="variants"><div class="sp-itm" title="Beden seçmek için tıklayınız">36</div><div class="sp-itm" title="Beden seçmek için tıklayınız">37</div><div class="selected sp-itm" title="Beden seçmek için tıklayınız">38</div><div class="sp-itm" title="Beden seçmek için tıklayınız">39</div><div class="sp-itm" title="Beden seçmek için tıklayınız">40</div></div></div><div class="product-button-container"><button class="add-to-basket" component-id="1"><div class="add-to-basket-button-text">Sepete Ekle</div><div class="add-to-basket-button-text-success">Sepete Eklendi</div><div class="add-to-bs-ldr"></div></button><div class="favorite-button"><div class="review-tooltip"><div class="tooltip-indicator"><button class="fv"><i class="i-heart"></i></button></div></div></div></div><aside class="delivery-favorite-info"></aside><div class="vas-product"></div><div class="featured-information" data-drroot="featured-information"><div class="featured-information-header">Öne Çıkan Özellikler:</div><div class="content-descriptions" data-drroot="content-descriptions"><ul id="content-descriptions-list"><li><span class="ellipse"></span><div class="productDetailSupplierPopup"><div class="popupBuffer"></div><div class="popupContent"><div class="popup-top"><div class="popup-logo"><i class="icon icon-trendyol-marketplace"></i></div><div class="popup-info"><div class="ttl">TRENDYOL PAZARYERİ</div><div class="description">Tüm satıcılarımız Trendyol hizmet standartlarını garanti eder.</div><div class="attributes"><div><i class="pdp-icon-reloaded"></i>Ücretsiz İade</div><div><i class="pdp-icon-cargo"></i> Hızlı Teslimat</div><div><i class="pdp-icon-phone"></i><span class="customer-support-text">Trendyol <br/>Müşteri Desteği</span></div></div></div></div><div class="supplier-info"><span>Satıcı:<b> BY Kotan Shoes </b></span><span>Satıcı Ünvanı:<b> YUSUF CEYLAN </b></span><span>İletişim:<b> Satıcının Trendyol tarafından teyit edilmiş e-posta ve iletişim adresi kayıt altındadır. </b></span><span><span id="cityInfo">Şehir:<b> İstanbul </b></span><span>Kep Adresi:<b> <a class="__cf_email__" data-cfemail="4039353335266e2325392c212e6e737400283370716e2b25306e3432" href="/cdn-cgi/l/email-protection">[email protected]</a> </b></span></span><span><span>Vergi Kimlik Numarası:<b> 2080876562 </b></span></span></div></div></div>Bu ürün <span class="product-description-market-place">BY Kotan Shoes</span> tarafından gönderilecektir.</li><li><span class="ellipse"></span>Kampanya fiyatından satılmak üzere 100 adetten fazla stok sunulmuştur.</li><li><span class="ellipse"></span>İncelemiş olduğunuz ürünün satış fiyatını satıcı belirlemektedir.</li><li><span class="ellipse"></span>Bir ürün, birden fazla satıcı tarafından satılabilir. Birden fazla satıcı tarafından satışa sunulan ürünlerin satıcıları ürün için belirledikleri fiyata, satıcı puanlarına, teslimat statülerine, ürünlerdeki promosyonlara, kargonun bedava olup olmamasına ve ürünlerin hızlı teslimat ile teslim edilip edilememesine, ürünlerin stok ve kategorileri bilgilerine göre sıralanmaktadır.</li><li><span class="ellipse"></span>Bu üründen en fazla 10 adet sipariş verilebilir. 10 adedin üzerindeki siparişleri Trendyol iptal etme hakkını saklı tutar. Belirlenen bu limit kurumsal siparişlerde geçerli olmayıp, kurumsal siparişler için farklı limitler belirlenebilmektedir.</li><li class="return-info"><span class="ellipse"></span>15 gün içinde ücretsiz iade. Detaylı bilgi için <a class="product-description-link" href="javascript:void(0)">tıklayın</a>.</li><li><span class="ellipse"></span>Beyaz Bağcıklı İnci Detaylı Kalın Taban Spor Ayakkabı Renk: Beyaz</li><li><span class="ellipse"></span>Taban Kalınlığı 5 cm dir.</li><li><span class="ellipse"></span>Tam Kalıptır.</li><li><span class="ellipse"></span>Yerli Üretim</li><li><span class="ellipse"></span>Materyal: Suni Deri</li><li><span class="ellipse"></span>İç Kısım: Sıcak Astar</li><li><span class="ellipse"></span>Rahat Ve Şık</li><li><span class="ellipse"></span>Bu Ürün BY Kotan Ayakkabı Tarafından gönderilecek.</li><li><span class="ellipse"></span>Bu spor ayakkabılar çok rahattır ve onları spor yapmak veya sadece dolaşmak için harika kılan kalın bir tabana sahiptir. Bağcıklı bir ön kısımları ve yanlarında inci detayı vardır. Klasik bir çift spor ayakkabı olan bu ayakkabılar, şık bir görünüm için inci detaylara ve kalın tabanlara sahiptir.</li><li><span class="ellipse"></span>Yüksek kaliteli malzemelerden üretilmiştir, günlük kullanım için yeterince rahat ve dayanıklıdır.</li><li><span class="ellipse"></span>Bağcıkli inci detaylı bir uyum sağlarken, kalın taban daha fazla destek ve stabilite sağlar.</li><li><span class="ellipse"></span>Çeşitli boyutlarda ve renklerde mevcuttur, herhangi bir gardıroba mükemmel bir katkı sağlarlar.</li><li><span class="ellipse"></span>Bu ayakkabılar spor ve gündelik giyim için tasarlanmıştır. Yürürken veya koşarken iyi destek ve konfor sağlayan kalın tabanları vardır. Ayakkabılar, onları dayanıklı kılan yüksek kaliteli malzemelerden yapılmıştır.</li></ul><div class="opacity-layout"></div></div><div><div class="all-features"><div class="opacity-layout"></div><div class="feature-buttons"><a class="button-all-features" rel="nofollow">ÜRÜNÜN TÜM ÖZELLİKLERİ<i class="i-chevron-right"></i></a></div><span class="line"></span></div></div></div></div>]
# # [<div class="product-detail-wrapper"><div class="pr-in-w"><div><div class="pr-in-cn"><div><h1 class="pr-new-br" data-drroot="h1"><a class="product-brand-name-with-link" href="/kotan-x-b158752">KOTAN</a> <span>Siyah Bağcıklı Inci Detaylı Kalın Taban Spor Ayakkabı</span></h1></div><div class="pr-in-ratings"></div><div class="social-proof-wrapper"><div class="socialProofWrapper" data-testid="social-proof"></div></div><div class="product-price-container"><div class="pr-bx-w"><div class="pr-bx-nm with-org-prc"><span class="prc-dsc">651,44 TL</span></div></div></div><div class="product-info-badges"><div class="installment-placeholder"></div></div></div></div></div><div class="slicing-attribute-placeholder" data-dr-hide="true"></div><div class="size-variant-wrapper size-variant-wrapper--without-expectation" data-drroot="size-variant"><div class="size-variant-title-wrapper"><span class="size-variant-title"><span class="size-variant-title--bold">Beden</span>: <span class="size-variant-attr-value">39</span></span></div><div class="variants"><div class="sp-itm" title="Beden seçmek için tıklayınız">36</div><div class="sp-itm" title="Beden seçmek için tıklayınız">37</div><div class="sp-itm" title="Beden seçmek için tıklayınız">38</div><div class="selected sp-itm" title="Beden seçmek için tıklayınız">39</div><div class="sp-itm" title="Beden seçmek için tıklayınız">40</div></div></div><div class="product-button-container"><button class="add-to-basket" component-id="1"><div class="add-to-basket-button-text">Sepete Ekle</div><div class="add-to-basket-button-text-success">Sepete Eklendi</div><div class="add-to-bs-ldr"></div></button><div class="favorite-button"><div class="review-tooltip"><div class="tooltip-indicator"><button class="fv"><i class="i-heart"></i></button></div></div></div></div><aside class="delivery-favorite-info"></aside><div class="vas-product"></div><div class="featured-information" data-drroot="featured-information"><div class="featured-information-header">Öne Çıkan Özellikler:</div><div class="content-descriptions" data-drroot="content-descriptions"><ul id="content-descriptions-list"><li><span class="ellipse"></span><div class="productDetailSupplierPopup"><div class="popupBuffer"></div><div class="popupContent"><div class="popup-top"><div class="popup-logo"><i class="icon icon-trendyol-marketplace"></i></div><div class="popup-info"><div class="ttl">TRENDYOL PAZARYERİ</div><div class="description">Tüm satıcılarımız Trendyol hizmet standartlarını garanti eder.</div><div class="attributes"><div><i class="pdp-icon-reloaded"></i>Ücretsiz İade</div><div><i class="pdp-icon-cargo"></i> Hızlı Teslimat</div><div><i class="pdp-icon-phone"></i><span class="customer-support-text">Trendyol <br/>Müşteri Desteği</span></div></div></div></div><div class="supplier-info"><span>Satıcı:<b> BY Kotan Shoes </b></span><span>Satıcı Ünvanı:<b> YUSUF CEYLAN </b></span><span>İletişim:<b> Satıcının Trendyol tarafından teyit edilmiş e-posta ve iletişim adresi kayıt altındadır. </b></span><span><span id="cityInfo">Şehir:<b> İstanbul </b></span><span>Kep Adresi:<b> <a class="__cf_email__" data-cfemail="5f262a2c2a39713c3a26333e31716c6b1f372c6f6e71343a2f712b2d" href="/cdn-cgi/l/email-protection">[email protected]</a> </b></span></span><span><span>Vergi Kimlik Numarası:<b> 2080876562 </b></span></span></div></div></div>Bu ürün <span class="product-description-market-place">BY Kotan Shoes</span> tarafından gönderilecektir.</li><li><span class="ellipse"></span>Kampanya fiyatından satılmak üzere 100 adetten fazla stok sunulmuştur.</li><li><span class="ellipse"></span>İncelemiş olduğunuz ürünün satış fiyatını satıcı belirlemektedir.</li><li><span class="ellipse"></span>Bir ürün, birden fazla satıcı tarafından satılabilir. Birden fazla satıcı tarafından satışa sunulan ürünlerin satıcıları ürün için belirledikleri fiyata, satıcı puanlarına, teslimat statülerine, ürünlerdeki promosyonlara, kargonun bedava olup olmamasına ve ürünlerin hızlı teslimat ile teslim edilip edilememesine, ürünlerin stok ve kategorileri bilgilerine göre sıralanmaktadır.</li><li><span class="ellipse"></span>Bu üründen en fazla 10 adet sipariş verilebilir. 10 adedin üzerindeki siparişleri Trendyol iptal etme hakkını saklı tutar. Belirlenen bu limit kurumsal siparişlerde geçerli olmayıp, kurumsal siparişler için farklı limitler belirlenebilmektedir.</li><li class="return-info"><span class="ellipse"></span>15 gün içinde ücretsiz iade. Detaylı bilgi için <a class="product-description-link" href="javascript:void(0)">tıklayın</a>.</li><li><span class="ellipse"></span>Renk: Siyah</li><li><span class="ellipse"></span>Taban Kalınlığı 5 cm dir.</li><li><span class="ellipse"></span>Tam Kalıptır. Yerli Üretim</li><li><span class="ellipse"></span>Materyal: Suni Deri</li><li><span class="ellipse"></span>İç Kısım: Sıcak Astar</li><li><span class="ellipse"></span>Rahat Ve Şık</li><li><span class="ellipse"></span>Bu Ürün BY Kotan Ayakkabı Tarafından gönderilecek.</li></ul><div class="opacity-layout"></div></div><div><div class="all-features"><div class="opacity-layout"></div><div class="feature-buttons"><a class="button-all-features" rel="nofollow">ÜRÜNÜN TÜM ÖZELLİKLERİ<i class="i-chevron-right"></i></a></div><span class="line"></span></div></div></div></div>]
#
