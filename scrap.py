

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import json
import urllib.request
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-gpu')
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
# options.add_argument("--headless")
options.add_argument("--disable-setuid-sandbox") 
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-dev-shm-usage")






class Scrap(object):
    def __init__(self):
        self.driver = webdriver.Chrome(
                    ChromeDriverManager().install(), options=options)
        self.wait = WebDriverWait(self.driver, 30)



    def scrap_data(self):
        self.driver.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/thead/tr/th[1]/a")))
        rows = self.driver.find_element_by_tag_name('table').find_elements_by_tag_name("tr")
        data_items = []
        attributes = ['Symbol', 'Security', 'SEC Filings', 'GIS Sector', 'GIS Sub Industry', 'Head Qaurters location',
                  'Date Added', 'CIK', 'Founded']
        for row_item in rows:
            for td in row_item.find_elements_by_tag_name("td"):
                print(td)
                data_items.append(''.join(td.text.split(',')))
        
        print(data_items)
    

scrapper = Scrap()
scrapper.scrap_data()