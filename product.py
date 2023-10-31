import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import utils


class Product:
    def __init__(self, driver: webdriver):
        self.driver = driver
        self.data = {}

    def get_name(self) -> str:
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'productTitle'))).text

    def get_image_urls(self):
        # TODO: need to capture all image url with all size
        image_urls = []
        image_url = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "span.a-list-item>span.a-declarative>div.imgTagWrapper>img.a-dynamic-image"))).get_attribute('src')
        image_urls.append(image_url)
        return image_urls

    def get_original_price(self):
        # TODO: get the original price, current code is fetch actual price
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#ppd .a-price span:nth-child(2)"))).text

    def get_price(self):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#ppd .a-price span:nth-child(2)"))).text

    def get_attributes(self):
        utils.expander_expand(self.driver, '#productOverview_feature_div')
        return utils.table_to_json(self.driver, '#productOverview_feature_div table')

    def get_description(self):
        # TODO decode unicode char
        utils.expander_expand(self.driver, '#productOverview_feature_div')
        return utils.ul_li_to_array(self.driver, '#featurebullets_feature_div ul')

    def get_technical_details_summary(self):
        return utils.table_to_json(self.driver, '#productDetails_techSpec_section_1')

    def get_technical_details_other(self):
        return utils.table_to_json(self.driver, '#productDetails_techSpec_section_2')

    def get_technical_details_additional_information(self):
        return utils.table_to_json(self.driver, '#productDetails_detailBullets_sections1')

    def get_customer_reviews(self):
        customer_reviews = []
        # {
        #     customer { name }
        #     review
        #     title
        #     country
        #     date
        #     description
        # }
        return customer_reviews

    def get_rating(self):
        final_rating = None
        total_rating = None
        pattern = r'(?P<rating>[0-9]*\.?[0-9]+) out of (?P<out_of>\d)'
        rating_out_of_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="rating-out-of-text"]'))).text
        match = re.search(pattern, rating_out_of_text)
        if match:
            final_rating = float(match.group('rating'))
            total_rating = int(match.group('out_of'))

        total_review_count = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="total-review-count"]'))).text
        customer_reviews_count = int(total_review_count.replace(' global ratings', ''))

        return {
            'final_rating': final_rating,
            'total_rating': total_rating,
            'rating_details': {
                '5': WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#histogramTable tr:nth-child(1) td:nth-child(3) a'))).text,
                '4': WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#histogramTable tr:nth-child(2) td:nth-child(3) a'))).text,
                '3': WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#histogramTable tr:nth-child(3) td:nth-child(3) a'))).text,
                '2': WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#histogramTable tr:nth-child(4) td:nth-child(3) a'))).text,
                '1': WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#histogramTable tr:nth-child(5) td:nth-child(3) a'))).text
            },
            'customer_reviews_count': customer_reviews_count,
            'customer_reviews': self.get_customer_reviews()
        }

    def scrape(self):
        self.data = {
            'name': self.get_name(),
            'image_urls': self.get_image_urls(),
            'original_price': self.get_original_price(),
            'price': self.get_price(),
            'attributes': self.get_attributes(),
            'description': self.get_description(),
            'rating': self.get_rating(),
            'technical_details': {
                'summary': self.get_technical_details_summary(),
                'other': self.get_technical_details_other(),
                'additional_information': self.get_technical_details_additional_information()
            }
        }
        return self.data
