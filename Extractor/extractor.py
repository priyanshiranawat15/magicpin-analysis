# webdriver imports and os import for setting driver path variable
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import Extracter.constants as const
# from selenium.webdriver.support.wait import WebDriverWait

# table extraction imports
from bs4 import BeautifulSoup
import pandas as pd

from custom_transformers import NanDropper, ColDropper, ReplaceNames, DateFormat, FloatInt, NameSeparator, HistoryColumns, RemoveAnomalies
from sklearn.pipeline import Pipeline

class InputFields(webdriver.Chrome):

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
        options.add_extension('C:/Users/Admin/AppData/Local/Google/Chrome/User Data/Default/Extensions/aapbdbdomjkkjkaonfhkkikfgjllcleb/2.0.13_0.crx')
        super(InputFields,self).__init__(options=options)
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
        self.get(const.BASE_URL)
    