import random
import string
import json
import os
import requests
import time
from dotenv import load_dotenv
from selenium.common import TimeoutException, NoSuchElementException, NoSuchAttributeException, \
    InvalidCookieDomainException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from VahanApp.VahanFlaskSelenium.utils import count_time
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


class GeneralException(Exception):
    pass


@count_time
def get_vehicle_details(browser, count, cookies_json):
    try:
        scrapper_elements = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.ID, "rcDetailsPanel"))
    except TimeoutException as error:
        raise GeneralException(error)
    registration_number = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                         "#rcDetailsPanel > div.box-background-section.font-bold > table > "
                                                         "tbody > tr:nth-child(1) > td:nth-child(1) > div").get_attribute(
        'innerText')
    vehicle_class = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                   "#rcDetailsPanel > div.box-background-section.font-bold > table > tbody > "
                                                   "tr:nth-child(2) > td > div").get_attribute('innerText')
    vehicle_fuel = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                  "#rcDetailsPanel > div.box-background-section.font-bold > table > tbody > "
                                                  "tr:nth-child(3) > td:nth-child(1) > div").get_attribute('innerText')
    model_name = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                "#rcDetailsPanel > div.box-background-section.font-bold > table > tbody > "
                                                "tr:nth-child(4) > td > div > span:nth-child(1)").get_attribute(
        'innerText')
    manufacturer_name = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                       "#rcDetailsPanel > div.box-background-section.font-bold > table > tbody "
                                                       "> tr:nth-child(4) > td > div > span:nth-child(3)").get_attribute(
        'innerText')
    registering_authority = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                           "#rcDetailsPanel > div.box-background-section.font-bold > table > "
                                                           "tbody > tr:nth-child(4) > td > div > span:nth-child(5)").get_attribute(
        'innerText')
    rc_status = scrapper_elements.find_element(By.CSS_SELECTOR,
                                               "#rcDetailsPanel > div.box-background-section.font-bold > table > tbody > "
                                               "tr:nth-child(1) > td:nth-child(2) > div > span").get_attribute(
        'innerText')
    emission_norms = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                    "#rcDetailsPanel > div.box-background-section.font-bold > table > tbody > "
                                                    "tr:nth-child(3) > td:nth-child(2) > div").get_attribute(
        'innerText')
    owner_name = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                "#rcDetailsPanel > div:nth-child(2) > div:nth-child(2)").get_attribute(
        'innerText')
    registration_date = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                       "#rcDetailsPanel > div:nth-child(2) > div:nth-child(4)").get_attribute(
        'innerText')

    # validity
    fitness_regn = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                  "#rcDetailsPanel > div:nth-child(5) > div:nth-child(2) > span").get_attribute(
        'innerText')
    pucc = scrapper_elements.find_element(By.CSS_SELECTOR,
                                          "#rcDetailsPanel > div:nth-child(6) > "
                                          "div.col-md-3.fit-width-content.font-bold.content-resize > span").get_attribute(
        'innerText')
    mv_tax = scrapper_elements.find_element(By.CSS_SELECTOR,
                                            "#rcDetailsPanel > div:nth-child(5) > div:nth-child(4)").get_attribute(
        'innerText')

    # insurance_details
    try:
        company_name = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                      "#rcDetailsPanel > div:nth-child(9) > span:nth-child(2)").get_attribute(
            'innerText')
        validity = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                  '#rcDetailsPanel > div:nth-child(9) > span:nth-child(4)').get_attribute(
            'innerText')
        policy_number = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                       '#rcDetailsPanel > div:nth-child(9) > span:nth-child(6)').get_attribute(
            'innerText')

    except (NoSuchElementException, NoSuchAttributeException):
        company_name = 'NA'
        validity = 'NA'
        policy_number = 'NA'

    # validity
    try:
        is_financed = scrapper_elements.find_element(By.CSS_SELECTOR,
                                                     '#rcDetailsPanel > div:nth-child(13) > div > span').get_attribute(
            'innerText')
    except (NoSuchElementException, NoSuchAttributeException):
        is_financed = 'NA'

    return {'registration_number': registration_number, 'RC_status': rc_status, 'vehicle_class': vehicle_class,
            'fuel': vehicle_fuel, 'emission_norms': emission_norms, 'model_name': model_name,
            'manufacturer_name': manufacturer_name, 'registering_authority': registering_authority,
            'owner_name': owner_name, 'registration_date': registration_date, 'fitness_regn': fitness_regn,
            'MV_tax': mv_tax, 'PUCC': pucc, 'Company_Name': company_name, 'Validity': validity,
            'Policy_Number': policy_number, 'Is_Financed': is_financed, 'Count': count, 'cookies_json': cookies_json}


@count_time
def solve_captcha(image_name):
    try:
        url = 'http://captcha.glossaryhub.co.in:9002/v1/api/process_captcha'
        with open(image_name, 'rb') as image:
            files = {'image': (image_name, image, 'multipart/form-data', {'Expires': '3600'})}
            with requests.Session() as s:
                response = s.post(url, files=files)
                res = json.loads(response.text)
                captcha = res['output']['captcha']['prediction']
        return captcha
    except KeyError:
        os.remove(image_name)


def get_random_string():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(10))


@count_time
def download_image(browser, image_name="vahancaptcha:ref_captcha"):
    try:
        image_element = WebDriverWait(browser, 1).until(lambda x: x.find_element(By.ID, image_name))
        image_name = f"/tmp/{get_random_string()}.png"
        image_element.screenshot(image_name)
        return image_name
    except StaleElementReferenceException:
        raise GeneralException("Captcha image is not rendering.")



@count_time
def add_vehicle_number(browser, vehicle_number, cookies=None):
    try:
        send_vehicle_ele = WebDriverWait(browser, 5).until(lambda x: x.find_element(By.ID, "regn_no1_exact"))
        send_vehicle_ele.send_keys(vehicle_number)
    except TimeoutException:
        GeneralException("Time Out for ADD vehical.")
    for _ in range(3):
        image_name = download_image(browser=browser)
        captcha = solve_captcha(image_name)
        captcha_element = browser.find_element(By.ID, "vahancaptcha:CaptchaID")
        captcha_ele = WebDriverWait(browser, 1).until(EC.visibility_of(captcha_element))
        captcha_ele.clear()
        captcha_ele.send_keys(str(captcha))

        search_count = browser.find_elements(By.TAG_NAME, 'label')
        count_ele = search_count[-1].get_attribute('innerText')
        count = int(count_ele) + 1

        all_button = browser.find_elements(By.TAG_NAME, 'button')
        button = all_button[2]
        WebDriverWait(browser, 1).until(EC.element_to_be_clickable(button))
        button.click()
        try:
            close_button = WebDriverWait(browser, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#userMessages > div > a")))
            close_button.click()
            reload_button = WebDriverWait(browser, 1).until(
                EC.element_to_be_clickable((By.ID, "vahancaptcha:btn_Captchaid")))
            reload_button.click()
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementClickInterceptedException):
            return get_vehicle_details(browser, count, cookies)
    raise GeneralException("API is not able to solve captcha.")


@count_time
def login_into_vahan(browser, vehicle_number, mobile_number, password):
    try:
        WebDriverWait(browser, 2).until(lambda x: x.find_element(By.ID, "TfMOBILENO")).send_keys(mobile_number)
        WebDriverWait(browser, 2).until(lambda x: x.find_element(By.ID, "btRtoLogin")).click()
    except TimeoutException as e:
        raise GeneralException("Failed to send mobile number.") from e
    try:
        password_input = WebDriverWait(browser, 1).until(lambda x: x.find_element(By.ID, "tfPASSWORD"))
        password_input.send_keys(password)
        browser.find_element(By.ID, "btRtoLogin").click()
    except TimeoutException as exc:
        raise GeneralException('Mobile number is not registered with NR Services Portal') from exc

    try:
        WebDriverWait(browser, 1).until(lambda x: x.find_element(By.ID, "regn_no1_exact"))
    except TimeoutException as err:
        raise GeneralException('Incorrect password or too many login attempts with this account') from err

    cookies = browser.get_cookies()
    cookies_json = json.dumps(cookies)
    return add_vehicle_number(browser, vehicle_number, cookies_json)


@count_time
def scrapper(vehicle_number, count, mobile_number, password, cookies, browser):
    browser.get('https://vahan.parivahan.gov.in/nrservices/faces/user/citizen/citizenlogin.xhtml')

    if count == 0 or count >= 5:
        return login_into_vahan(browser, vehicle_number, mobile_number, password)
    return add_cookies_in_browser(cookies, browser, vehicle_number, mobile_number, password)


@count_time
def add_cookies_in_browser(cookies, browser, vehicle_number, mobile_number, password):
    try:
        browser.delete_all_cookies()
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.refresh()
        url = 'https://vahan.parivahan.gov.in/nrservices/faces/user/citizen/searchstatus.xhtml'
        browser.execute_script(f"window.location.href = '{url}'")
        WebDriverWait(browser, 1).until(lambda x: x.find_element(By.ID, "regn_no1_exact"))
        return add_vehicle_number(browser, vehicle_number, None)
    except (InvalidCookieDomainException, TimeoutException):
        return login_into_vahan(browser, vehicle_number, mobile_number, password)
