# webdriver imports and os import for setting driver path variable
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# from selenium.webdriver.support.wait import WebDriverWait

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
        try:
            self.get(BASE_URL)
            time.sleep(3)
        except e:
            print("Page blocked")

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
                time.sleep(1)
        except e:
            print("Sublisting header not found on the webpage. ")


    def add_item(self, name):
        try:
            print("finding item to add")
            items = self.find_elements(By.CLASS_NAME, 'categoryItemHolder')
            for item in items:
                print("item \n\n")
                if item.find_element(By.CLASS_NAME,'itemName').get_attribute('innerText') == name:
                    print("item found\n")
                    holder = item.find_element(By.CLASS_NAME,'itemCountHolder')
                    print("holder found\n")
                    div_1 = holder.find_element(By.TAG_NAME,'div')
                    print("div found\n")
                    button = div_1.find_element(By.TAG_NAME, 'button')
                    print("button found\n")
                    button.click()
                    print("button clicked")
                    time.sleep(1)
                    self.find_element(By.TAG_NAME,'addCTA').click()
                    break
            time.sleep(2)
        except e:
            print(f"Item {name} not found on the page")
    
    def extract_discounted_price(self):
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
            div_element = self.find_element(By.CLASS_NAME,'finalPrice')
            print(f"Final price after discount: {div_element.text()}")
        except e:
            print("Add items to discover the discounted price element")

#for code modularity, below code can be a separate run.py file with imports of Extractor class 
with Extractor() as e:
    e.landing_page()
    e.click_dropdowns()
    e.add_item(name="Butter Paneer Kulcha Burger")
    e.extract_discounted_price()
