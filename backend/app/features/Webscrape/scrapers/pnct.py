from .baseModel import BaseTerminalScraper
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from typing import Dict, Type, Optional, Literal, List
import time

class PNCTScraper(BaseTerminalScraper):
    url = "https://www.pnct.net/TosInquiry"

    def __init__(self, driver, containers = None):
        super().__init__(driver)
        self.contaienr = containers
    def open_page(self):
        self.get(self.url)
    
    def importAvailability(self):
        try:
            self.select_xpath("InquiryType", "ContainerAvailabilityByCntr")
        except TimeoutException:
            print("Timed out waiting enterContainer")

    def enterContainer(self, containers: Optional[List] = None):
        if containers is None:
            return ""  # or handle the empty case as needed
        string = ""
        for container in containers:
            string += container + "\n"
        
        print(string)

        input_xpath = (
            "//h3[.//strong[normalize-space()='Quick Lookup']]"
            "/ancestor::div[contains(@class,'view')]"
            "/following-sibling::div"
            "//textarea | //input[contains(@class,'mat-input-element')]"
        )

        self.type_xpath(input_xpath, string)
        
        print("typed")

        self.click_xpath('//*[@id="btnTosInquiry"]')


    
    def scrape_container_status(self):
        try:
            self.open_page()
            self.importAvailability()
            container = ['GAOU6438551']
            self.enterContainer(container)
            time.sleep(15)
        finally:
            self.driver.quit()