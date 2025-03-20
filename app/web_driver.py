from selenium import webdriver
from selenium_stealth import stealth


class WebDriver:
    def __enter__(self):
        self.webdriver = webdriver.Chrome(options=self.get_options())
        stealth(self.webdriver,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.105 Safari/537.36',
                languages=['en-US', 'en'],
                vendor='Google Inc.',
                platform='Win32',
                webgl_vendor='Intel Inc.',
                renderer='Intel Iris OpenGL Engine',
                fix_hairline=True,
                )
        return self.webdriver

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.webdriver.quit()

    def get_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--blink-settings=imagesEnabled=false')
        # options.add_experimental_option('detach', True)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        return options
