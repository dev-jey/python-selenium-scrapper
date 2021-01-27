'''Imports for used packages'''
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


''' Set up selenium options'''
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")


class Scrap(object):
    '''Class to handle all the scrapping process'''
    def __init__(self):
        '''Initialize driver and wait instances'''
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
        self.wait = WebDriverWait(self.driver, 30)


    def scrap_data(self):
        '''Make request to wikipedia for site map'''
        self.driver.get(
            'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        # Wait until the table is visible
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/thead/tr/th[1]/a")))
        
        # Get all rows from the constituents table
        rows = self.driver.find_element_by_id(
            'constituents').find_elements_by_tag_name("tr")

        # Define the columns for the data frame
        attributes = ['Symbol', 'Security', 'SEC Filings', 'GIS Sector', 'GIS Sub Industry', 'Head Qaurters location',
                      'Date Added', 'CIK', 'Founded']

        all_first_table_data = self.organize_table_data(rows, attributes)
        
        df = pd.DataFrame.from_dict(all_first_table_data)
        # Drop all null records in dataframe
        df.dropna(inplace=True)
        # Select only the needed columns
        df1 = df[['Symbol', 'Security', 'CIK', 'GIS Sector', 'GIS Sub Industry']]
        # Rename the columns
        df1.columns = ['Ticker', 'Company Name', 'CIK', 'General Industry', 'Sub Industry']
        # Write the data to excel file called companies
        writer = pd.ExcelWriter('companies.xlsx', engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='Sheet2', index=False)
        writer.save()

    def organize_table_data(self, rows, attributes):
        # Organize the retrieved table data by matching columns with respective table data
        all_data = []
        for row_item in rows:
            data_items = []
            for td in row_item.find_elements_by_tag_name("td"):
                data_items.append(''.join(td.text.split(',')))
                detail = dict(zip(attributes, data_items))
                all_data.append(detail)
        return all_data

# Create an instance of the Scrap class and call the scrap_data method
scrapper = Scrap()
scrapper.scrap_data()
