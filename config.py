import os
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv(find_dotenv())


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'


def make_instance():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def make_driver_dict():
    my_driver = {}
    number_drivers = int(os.getenv('NUMBER_DRIVERS'))
    for i in range(number_drivers):
        driver = make_instance()
        my_driver[f'driver_{i}'] = driver
    return my_driver
