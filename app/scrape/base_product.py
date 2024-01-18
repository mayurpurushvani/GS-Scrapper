import re
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app import utils
from app.model.product import Product as ProductModel


class BaseProduct:
    def __init__(self, driver: webdriver, link):
        self.driver = driver
        self.link = link
        self.data = {}

    def get_name(self):
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
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#corePrice_desktop span.a-price[data-a-strike=\"true\"]"))).text

    def get_price(self):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#corePrice_desktop span.a-price:not([data-a-strike=\"true\"])"))).text

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

    def get_review(self, review):
        utils.expander_expand(review, '', 'Read more')

        country = None
        date = None
        pattern = r'Reviewed in the (?P<country>.*) on (?P<date>.*)'
        review_date = WebDriverWait(review, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="review-date"]'))).text
        match = re.search(pattern, review_date)
        if match:
            country = match.group('country')
            date = datetime.strptime(match.group('date'), '%B %d, %Y').strftime('%Y-%m-%d')

        rating = None
        pattern = r'(?P<rating>[0-9]*\.?[0-9]+) out of (?P<out_of>\d)'
        review_star_rating = WebDriverWait(review, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="review-star-rating"]'))).get_attribute(
            'textContent')
        match = re.search(pattern, review_star_rating)
        if match:
            rating = float(match.group('rating'))

        return {
            'id': review.get_attribute('id'),
            'customer_name': WebDriverWait(review, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.a-profile-name'))).text,
            'rating': rating,
            'title': WebDriverWait(review, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="review-title"] span:nth-child(3)'))).text,
            'country': country,
            'date': date,
            'description': WebDriverWait(review, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="review-collapsed"]'))).text
        }

    def get_customer_reviews(self):
        customer_reviews = []
        reviews = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-hook="review"]')))
        for review in reviews:
            customer_reviews.append(self.get_review(review))
        return customer_reviews

    def get_rating(self):
        final_rating = None
        pattern = r'(?P<rating>[0-9]*\.?[0-9]+) out of (?P<out_of>\d)'
        rating_out_of_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="rating-out-of-text"]'))).text
        match = re.search(pattern, rating_out_of_text)
        if match:
            final_rating = float(match.group('rating'))

        total_review_count = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hook="total-review-count"]'))).text
        customer_reviews_count = int(total_review_count.replace(' global ratings', ''))

        return {
            'final_rating': final_rating,
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

    def get_related_asin(self):
        return ''

    def scrape(self):
        self.driver.get(self.link.link)
        # TODO [Products related to this item ASIN]
        # TODO open variant wise product
        self.data = {
            'sku': self.link.asin,
            'name': self.get_name(),
            'description': ','.join(self.get_description()),
            'sale_price': utils.string_price_to_float(self.get_price()),
            'regular_price': utils.string_price_to_float(self.get_original_price()),
            'images': ','.join(self.get_image_urls()),
            'external_url': self.link.link,
            # 'attributes': self.get_attributes(),
            # 'rating': self.get_rating(),
            # 'technical_details': {
            #     'summary': self.get_technical_details_summary(),
            #     'other': self.get_technical_details_other(),
            #     'additional_information': self.get_technical_details_additional_information()
            # },
            # 'related_asin': self.get_related_asin()
        }
        technical_details = self.get_technical_details_other()
        weight = utils.get_weight(technical_details)
        self.data['weight'] = weight
        dimensions = utils.get_dimensions(technical_details)
        self.data['length'] = dimensions['length']
        self.data['width'] = dimensions['width']
        self.data['height'] = dimensions['height']
        self.store()

    def store(self):
        ProductModel.bulk_create([self.data])
