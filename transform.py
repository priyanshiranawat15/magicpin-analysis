# webdriver imports and os import for setting driver path variable
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# table extraction imports
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://magicpin.in/New-Delhi/Paharganj/Restaurant/Eatfit/store/61a193/delivery/'
class Extractor(webdriver.Chrome):

    def __init__(self, driver_path="G:/SeleniumDrivers" ,teardown=False):
        '''
        input-
            driver_path(PATH): specifies path to chromedriver.exe
            teardown(boolean): if true, browser will not close after opening the landing page
        function -
            initializes the driver and sets the driver path in os environment
            sets the teardown variable to prevent browser from closing immediately
        '''
        self.driver_path = driver_path
        self.teardown = teardown #prevents webpage from closing immediately
        os.environ['PATH'] += self.driver_path #sets driver path in os environments
        options = webdriver.ChromeOptions()
        super(Extractor,self).__init__(options=options)
        self.maximize_window()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        function- 
            prevents browser from closing
        '''
        if self.teardown:
            self.quit()
        else:
            while(True): #browser keeps on closing after opening, hence I thought of this idea, if i keep loop running, then it won't close the browser
                pass

    def landing_page(self):
        '''
        function -
            driver launches the landing page
        '''
        self.get(BASE_URL)
        time.sleep(3)

    def click_dropdowns(self):
        """
        Clicks on all dropdown headers in the web page to reveal hidden content.

        This function iterates through all dropdown headers identified by the class 'subListingsHeader'
        and simulates a click action on each header, causing the associated content to be displayed.

        Parameters:
            None

        Returns:
            None
        """
        try:
            dropdown_headers = self.find_elements(By.CLASS_NAME,'subListingsHeader')
            for dropdown in dropdown_headers:
                dropdown.click()
                WebDriverWait(self, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'categoryItemHolder')))
        except e:
            print("Sublisting header not found on the webpage. ")

    def click_more_btns(self):
        try:
            btns = self.find_elements(By.XPATH, "//*[contains(text(), '... more')]")
            
            self.execute_script("window.scrollTo(0,0)")
            for b in btns:
                b.click()
        except e:
            print("Sublisting header not found on the webpage. ")

    def extract_soup_object(self):
        """
        Extracts a BeautifulSoup object from a specified div element and prints its text content.

        This function retrieves the outer HTML content of a specific div element identified by the class
        'catalogItemsHolder' using Selenium. It then creates a BeautifulSoup object and prints its text content.

        Parameters:
            None

        Returns:
            None
        """
        try:
            div_element = self.find_element(By.CLASS_NAME, 'catalogItemsHolder').get_attribute("outerHTML")
            soup = BeautifulSoup(div_element, 'html.parser')
            print('Soup initialized\n\n')

            food_items = []
            for category in soup.find_all('article', 'categoryListing'):
                category_name = category.find('h4', 'categoryHeading').text.strip()
                for item in category.find_all('section', class_='categoryItemHolder'):
                    food_name = item.find('p', class_='itemName').text.strip()
                    food_price = item.find('span', class_='itemPrice').text.strip()
                    food_desc = item.find('section', class_='description').text.strip()
                    food_items.append({'Food': food_name, 'Price': food_price, 'Category': category_name, 'Desc': food_desc})

            return food_items
        except Exception as e:
            print(f"Error in extracting soup object: {e}")
            return []
    
    def data_cleaner(self,food_items, drop_duplicates=True, price_to_numeric=True, use_description=True, drop_nan=True):
        try:
            df = pd.DataFrame(food_items)
            if drop_duplicates:
                df.drop_duplicates(inplace=True)

            if price_to_numeric:
                df['Price'] = pd.to_numeric(df['Price'].str.replace('₹', '').replace(',', ''), errors='coerce')

            if drop_nan:
                df.dropna(inplace=True)

            if not use_description:
                df.drop(['Desc'], inplace=True, axis=1)

            return df
        except Exception as e:
            print(f"Error in data cleaning: {e}")
            return pd.DataFrame()

    def to_csv(self, df, name):
        try:
            df.to_csv(f'{name}.csv', index=False)
            print(f"Data successfully saved to {name}.csv")
        except Exception as e:
            print(f"Error in saving to CSV: {e}")


#for code modularity, below code can be a separate run.py file with imports of Extractor class 
if __name__ == "__main__":
    with Extractor() as e:
        try:
            e.landing_page()
            e.click_dropdowns()
            e.click_more_btns()
            items = e.extract_soup_object()
            if items:
                df = e.data_cleaner(food_items=items)
                if not df.empty:
                    e.to_csv(df=df, name='food_menu')
        except Exception as e:
            print(f"An error occurred: {e}")