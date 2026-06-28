import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class ScraperHiringCafe:
    """
    Clase para extraer ofertas de trabajo de HiringCafe
    """
    
    def __init__(self, url="https://hiring.cafe/"):
        self.url = url
        self.ofertas = []
        self.driver = None