from .baseModel import BaseTerminalScraper
from selenium.common.exceptions import TimeoutException
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

    
    def enterContainer(self):
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
                '//*[@id="cdk-accordion-child-2"]/div/span[1]/mat-card'
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
    
    def script_login(self):
        try:
            self.login()
            self.enterContainer()
            time.sleep(10)
        finally:
            self.driver.quit()
