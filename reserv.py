import requests

login_url = (
    "https://genclikspor.antalya.bel.tr/sporkursiyer/moduller/kontrol/giriskontrol.jsp"
)
reservation_url = "https://genclikspor.antalya.bel.tr/sporkursiyer/moduller/rezervasyonlar/yenirezervasyonp.jsp"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Referer": "https://genclikspor.antalya.bel.tr/sporkursiyer/index.jsp",
}
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
#     "Referer": "https://genclikspor.antalya.bel.tr/sporkursiyer/index.jsp",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Connection": "keep-alive"
# }
amin = {"tckimlikno": "99111724318", "sifre": "123456"}
niki = ["99789701864", "09.09.1981"]
rasol = {"tckimlikno": "50077919378", "sifre": "92042500"}
khanomrasol = ["50079419432", "22.02.1986"]

login_params = rasol
date = "2024.10.01"
time = "19:00 - 20:00"
session = requests.Session()

login_response = session.get(login_url, headers=headers, params=login_params)

if login_response.status_code == 200:
    if "JSESSIONID" in session.cookies:
        print("کوکی JSESSIONID با موفقیت دریافت شد:", session.cookies.get("JSESSIONID"))
        if login_params == amin:
            reservation_data = {
                "rezervasyonsalonu": "4",
                "rezervasyontarihi": date,
                "rezervasyonsaati": time,
                "tckimlikno": "99111724318",
                "adisoyadi": "AMİN AGHİLİ",
                "epostaadresi": "aghili.amin@gmail.com",
                "ceptelefonu": "5525097182",
                "tckimlikno2": niki[0],
                "dogumtarihi2": niki[1],
                "tckimlikno3": "",
                "dogumtarihi3": "",
                "tckimlikno4": "",
                "dogumtarihi4": "",
            }
        if login_params == rasol:
            reservation_data = {
                "rezervasyonsalonu": "4",
                "rezervasyontarihi": date,
                "rezervasyonsaati": time,
                "tckimlikno": "50077919378",
                "adisoyadi": "RASOUL AMİNİ",
                "epostaadresi": "rasoulamini8047@gmail.com",
                "ceptelefonu": "5367088078",
                "tckimlikno2": khanomrasol[0],
                "dogumtarihi2": khanomrasol[1],
                "tckimlikno3": "",
                "dogumtarihi3": "",
                "tckimlikno4": "",
                "dogumtarihi4": "",
            }

        reservation_response = session.post(
            reservation_url, headers=headers, data=reservation_data
        )

        if reservation_response.status_code == 200:
            print("رزرو با موفقیت انجام شد")
        else:
            print("خطا در رزرو:", reservation_response.status_code)
    else:
        print("کوکی JSESSIONID دریافت نشد")
else:
    print("ورود به سیستم ناموفق بود:", login_response.status_code)
