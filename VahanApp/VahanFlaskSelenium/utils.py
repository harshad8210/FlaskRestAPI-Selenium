import time
import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from VahanApp.VahanFlaskSelenium.model import Cookies


def count_time(func):
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


def get_web_driver(driver_dict, working_drivers):
    for driver in driver_dict:
        if driver not in working_drivers:
            working_drivers.append(driver)
            return driver, driver_dict[driver], working_drivers
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    return 'New', webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options), working_drivers


def get_id_pass():
    """Get login credentials from json"""
    with open('Credentials.json') as f:
        data = json.load(f)

    """ Access the credentials array """
    credentials = data['credentials']

    # Choose a random set of credentials from the array
    random_creds = random.choice(credentials)

    return random_creds['mobile_number'], random_creds['password']


def get_cookies_database(driver_name):
    """Get cookies from the database"""
    cookies = Cookies.get_cookies(driver_name)

    selenium_cookies = []
    for d_cookie in cookies:
        cookie = {
            "domain": d_cookie.domain,
            "httpOnly": d_cookie.httpOnly,
            "name": d_cookie.name,
            "path": d_cookie.path,
            "sameSite": d_cookie.sameSite,
            "secure": d_cookie.secure,
            "value": d_cookie.value
        }
        selenium_cookies.append(cookie)

    return cookies, selenium_cookies
