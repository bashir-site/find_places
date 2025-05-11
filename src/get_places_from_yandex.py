from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd


def scrape_yandex_maps(query, city):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(f"https://yandex.ru/maps/?text={query}+{city}")

        page.wait_for_selector(".search-business-snippet-view")
        html = page.inner_html(".search-business-snippet-view__content")
        soup = BeautifulSoup(html, "html.parser")

        businesses = []
        for item in soup.select(".search-business-snippet-view"):
            name = item.select_one(".search-business-snippet-view__title").text.strip()
            address = item.select_one(".search-business-snippet-view__address").text.strip()
            phone = item.select_one(".business-contacts-view__phone").text.strip() if item.select_one(
                ".business-contacts-view__phone") else "Нет данных"
            website = item.select_one(".business-urls-view__text")  # Блок с сайтом

            if not website:  # Если сайта нет
                businesses.append({
                    "Название": name,
                    "Адрес": address,
                    "Телефон": phone
                })

        browser.close()
        return businesses


# Пример использования
data = scrape_yandex_maps("кафе", "Москва")
df = pd.DataFrame(data)
df.to_csv("no_website_cafes.csv", index=False)
print(f"Сохранено {len(df)} заведений.")
