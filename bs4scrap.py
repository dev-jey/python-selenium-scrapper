'''Imports for used packages'''
import requests
import pandas as pd
from bs4 import BeautifulSoup



class Scrap(object):
    '''Class to handle all the scrapping process'''
    def __init__(self):
        '''Make request to wikipedia for site map'''
        self.page = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        self.soup = BeautifulSoup(self.page.content, 'html.parser')


    def scrap_data(self):
        # Get all rows from the constituents table
        rows = self.soup.find('table', id='constituents').find_all("tr")

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
            for td in row_item.find_all("td"):
                data_items.append(''.join(td.text.split(',')))
                detail = dict(zip(attributes, data_items))
                all_data.append(detail)
        return all_data

# Create an instance of the Scrap class and call the scrap_data method
scrapper = Scrap()
scrapper.scrap_data()
