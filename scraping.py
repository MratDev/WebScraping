import sys
sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class Flyer:
    def __init__(self, title, thumbnail, shop_name, valid_from, valid_to, parsed_time):
        self.title = title
        self.thumbnail = thumbnail
        self.shop_name = shop_name
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.parsed_time = parsed_time

    def __repr__(self):
        return f"Flyer({self.title}, {self.shop_name}, {self.valid_from} - {self.valid_to})"

class FlyerScraper:
    def __init__(self, url):
        self.url = url
        self.flyers = []
        self.flyers_count = 0
        self.driver = self.init_driver()

    def init_driver(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def parse_hypermarkets(self):
        self.driver.get(self.url)
        time.sleep(2)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        hypermarket_list = soup.find('ul', class_='list-unstyled categories').find_all('a')

        for market in hypermarket_list:
            transfer = market['href']
            shop_name = market.text.strip()
            transfer_url = self.url.removesuffix('/hypermarkte/') + transfer
            print(f'Parsing {shop_name} from {transfer_url}')
            self.parse_flyers_for_shop(transfer_url, shop_name)

    def parse_flyers_for_shop(self, transfer_url, shop_name):
        self.driver.get(transfer_url)
        time.sleep(2)
        page_source = self.driver.page_source
        website_soup = BeautifulSoup(page_source, 'html.parser')

        letaky_grid = website_soup.find('div', class_='letaky-grid')
        if not letaky_grid:
            print(f"Warning: Could not find flyer container for {shop_name}")
            return

        item_divs = letaky_grid.find_all('div', class_=lambda x: x and 'brochure-thumb' in x)
        print(f"Found {len(item_divs)} potential flyers for {shop_name}")

        for item in item_divs:
            self.process_flyer(item, shop_name)

    def process_flyer(self, item, shop_name):
        try:
            title = item.find('p', class_='grid-item-content')
            title = title.text.strip() if title else '-'

            picture = item.find('picture')
            if picture and picture.find('img'):
                thumbnail = picture.find('img')
                thumbnail = thumbnail.get('src', thumbnail.get('data-src', '-')) if thumbnail else '-'
            else:
                thumbnail = item.find('img')
                thumbnail = thumbnail.get('src', thumbnail.get('data-src', '-')) if thumbnail else '-'

            validity = item.find('small', class_='hidden-sm')
            validity = validity.text.split(' - ') if validity else ['-', '-']
            if len(validity) == 1:
                validity.append('-')

            now = datetime.now()
            parsed_date = now.strftime("%Y-%m-%d") 

            try:
                valid_from = datetime.strptime(validity[0].strip(), "%d.%m.%Y").strftime("%Y-%m-%d")
            except ValueError:
                valid_from = '-'
            try:
                valid_to = datetime.strptime(validity[1].strip(), "%d.%m.%Y").strftime("%Y-%m-%d")
            except ValueError:
                valid_to = '-'

            if valid_from == '-':
                try:
                    a_tag = item.find('a')
                    if a_tag and 'title' in a_tag.attrs:
                        valid_from = datetime.strptime(a_tag['title'].split()[-1], "%d.%m.%Y").strftime("%Y-%m-%d")
                        valid_to = '-'
                except (ValueError, TypeError, AttributeError):
                    valid_from = '-'

            flyer = Flyer(title, thumbnail, shop_name, valid_from, valid_to, now.strftime("%Y-%m-%d %H:%M:%S"))
            print(flyer)
            if valid_from != '-' and valid_from <= parsed_date and (valid_to == '-' or parsed_date <= valid_to):
                self.flyers.append(flyer)
                self.flyers_count += 1
        except Exception as e:
            print(f"Error processing flyer: {e}")

    def save_to_json(self):
        with open('flyers_data.json', 'w', encoding='utf-8') as f:
            json.dump([flyer.__dict__ for flyer in self.flyers], f, ensure_ascii=False, indent=4)
        print('Data saved to flyers_data.json')

    def quit_driver(self):
        self.driver.quit()

def main():
    url = 'https://www.prospektmaschine.de/hypermarkte/'
    scraper = FlyerScraper(url)
    scraper.parse_hypermarkets()
    scraper.save_to_json()
    scraper.quit_driver()

if __name__ == '__main__':
    main()