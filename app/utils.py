import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def expander_expand(driver, expander_selector, text_label='See more'):
    expander = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '{} .a-expander-prompt'.format(expander_selector))))
    if expander.text == text_label:
        expander.click()


def table_to_json(driver, table_selector):
    data = {}
    rows = WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, '{} tr'.format(table_selector))))
    for row in rows:
        cols = WebDriverWait(row, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'th, td')))
        is_key = True
        key = None
        for col in cols:
            if is_key:
                key = col.text
                is_key = False
            elif key is not None:
                data[key] = col.text
    return data


def ul_li_to_array(driver, ul_selector):
    data = []
    lis = WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, '{} li'.format(ul_selector))))
    for li in lis:
        data.append(li.text)
    return data


def string_price_to_float(price):
    return float(price.replace('$', ''))


def get_weight(technical_details):
    for key, value in technical_details.items():
        if 'Weight' in key:
            return float(re.sub('[^0-9.]', '', value))


def get_dimensions(technical_details):
    for key, value in technical_details.items():
        if 'Product Dimensions' in key:
            return decode_dimensions(value)
    for key, value in technical_details.items():
        if 'Dimensions' in key:
            return decode_dimensions(value)


def decode_dimensions(dimensions_string):
    dimensions = {'length': None, 'width': None, 'height': None}
    regex = r"(?P<length>[0-9.]*) x (?P<width>[0-9.]*) x (?P<height>[0-9.]*)"
    matches = re.search(regex, dimensions_string)
    if matches:
        dimensions = matches.groupdict()
    return dimensions
