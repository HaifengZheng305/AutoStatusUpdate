from .baseModel import BaseTerminalScraper
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from typing import Dict, Type, Optional, Literal, List
import time

class MaherScraper(BaseTerminalScraper):
    url = "https://mahercsp.maherterminals.com/CSP/"

    def __init__(self, driver, username, password, containers = None):
        super().__init__(driver, containers=containers)
        self.username = username
        self.password = password

    def login(self):
        try:
            self.get(self.url)
            self.type("input[formcontrolname='username']", self.username)
            print("username entered")
            self.type("input[formcontrolname='password']", self.password)
            print("password entered")
            self.click_xpath("//button[.//span[contains(text(), 'Login')]]")##this is the login button
            print("logged in")
        except TimeoutException:
            print("Timed out waiting for username/password field")
            print("Final URL:", self.driver.current_url)
            # dump HTML so you can see what Selenium sees

    
    def importAvailability(self):
        try:
            self.wait_xpath('//*[@id="noPrint"]')
            print("new page loaded")
            # 1. Click "Menu"

        #     # 2. Click the “Equipment” accordion header
            self.ensure_expanded_xpath(
                header_xpath='//*[@id="noPrint"]/mat-toolbar-row/button[1]',
                inner_xpath='//*[@id="mat-expansion-panel-header-2"]',
                timeout=8
            )

            print("menu ensured expanded")
        #     self.wait_xpath('//*[@id="menuCanvas"]/span[2]/mat-card/div/button')

            self.click_xpath( 
                '//*[@id="mat-expansion-panel-header-2"]'
            )
            print("clicked Equipment")

            self.ensure_expanded_xpath(
                header_xpath='//*[@id="mat-expansion-panel-header-2"]',
                inner_xpath='//*[@id="cdk-accordion-child-2"]/div/span[1]/mat-card',
                timeout=8
            )

            print("container Availability Clicked ensured expanded")

            self.click_xpath( 
                '//*[@id="cdk-accordion-child-2"]/div/span[2]/mat-card'
            )

            print("clicked Import Availability")

        #     # 3. Now click the “Import Availability” item under Equipment
        #     # import_avail_xpath = (
        #     #     "//*[@id='noPrint']//mat-expansion-panel"
        #     #     "[.//mat-expansion-panel-header//div[contains(normalize-space(.), 'Equipment')]]"
        #     #     "//button[.//span[contains(normalize-space(.), 'Import Availability')]]"
        #     # )
            
        #     # self.wait_xpath(
        #     #     import_avail_xpath
        #     # )

        #     # self.click_xpath(
        #     #     import_avail_xpath
        #     # )
        #     # print("clicked Import Availability")


        except TimeoutException:
            print("Timed out waiting enterContainer")
            print("Final URL:", self.driver.current_url)
            # dump HTML so you can see what Selenium sees

    def scrape_container_status(self, container_id: str) -> dict:
        self.get("https://mahercsp.maherterminals.com/CSP/")

    def enterContainer(self, containers: Optional[List] = None):
        if containers is None:
            return ""  # or handle the empty case as needed
        string = ""
        for container in containers:
            string += container + "\n"
        
        print(string)

        self.type_xpath('//*[@id="mat-input-2"]', string)
        
        print("typed")

        self.click_xpath("//button[.//span[text()='Search']]")

    def extract_containers(self):
        self.wait_CSS( "mat-row.mat-row")

    # Wait until table rows are rendered

        rows = self.driver.find_elements(By.CSS_SELECTOR, "mat-row.mat-row")

        containers = []

        for row in rows:
            def safe_text(selector):
                try:
                    el = row.find_element(By.CSS_SELECTOR, selector)
                    txt = el.text.strip()
                    return txt if txt else None
                except:
                    return None

            container_id = safe_text(".mat-column-container")

            # Available column (greenColor = Yes, redColor/empty = No)
            available_text = safe_text(".greenColor")
            available = True if available_text == "Yes" else False

            customs_release = safe_text(".mat-column-customs_released_description")

            freight_release_text = safe_text(".mat-column-freight_released_fmt")
            freight_release = (
                True if freight_release_text == "Yes"
                else False if freight_release_text is not None
                else None
            )

            last_free_day = safe_text(".mat-column-fte_date_fmt")

            # Skip empty / invalid rows
            if not container_id:
                continue

            containers.append({
                "container": container_id,
                "available": available,
                "customs_release": customs_release,
                "freight_release": freight_release,
                "last_free_day": last_free_day
            })

        return containers

        
        
    
    def scrape_container_status(self):
        try:
            self.login()
            self.importAvailability()
            container = ['OOLU0192235', 'OOLU0701076', 'SEGU1924857', 'SEGU2028705', 'TEMU0517730']
            self.enterContainer(container)
            result = self.extract_containers()
            print(result)
            time.sleep(15)
        finally:
            self.driver.quit()
