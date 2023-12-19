from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebDriver:
    def __enter__(self):
        self.webdriver = webdriver.Chrome(options=self.get_options(), service=Service(ChromeDriverManager().install()))
        self.webdriver.request_interceptor = self.request_interceptor
        return self.webdriver

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.webdriver.quit()

    def get_options(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')
        # options.add_argument('--blink-settings=imagesEnabled=false')
        # options.add_experimental_option('detach', True)
        return options

    def request_interceptor(self, request):
        request.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
        request.headers["Accept-Encoding"] = "gzip, deflate"
        request.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        request.headers["DNT"] = "1"
        request.headers["Connection"] = "close"
        request.headers["Upgrade-Insecure-Requests"] = "1"
