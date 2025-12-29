from .baseModel import BaseTerminalScraper
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from typing import Dict, Type, Optional, Literal, List
from app.models.container import Container, TerminalName
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

        self.click_xpath('//*[@id="btnTosInquiry"]')

    def extract_containers(self):
        self.wait_xpath("//tbody/tr[contains(@class,'ng-scope')]")

        rows = self.driver.find_elements(
            By.XPATH, "//tbody/tr[contains(@class,'ng-scope')]"
        )

        results = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")

            def text_or_none(idx):
                txt = cols[idx].text.strip()
                return txt if txt else None

            container = Container(
                container_number=text_or_none(0),
                available=BaseTerminalScraper.parse_available(text_or_none(1)),
                customs_release=BaseTerminalScraper.parse_bool(text_or_none(4)),
                freight_release=BaseTerminalScraper.parse_bool(text_or_none(5)),
                last_free_day=BaseTerminalScraper.parse_date(text_or_none(8)),
                terminal= TerminalName.PNCT
            )

            results.append(container)

        return results



    
    def scrape_container_status(self):
        print("PNCT")
        self.open_page()
        self.importAvailability()
        container = ['GAOU6438551', 'JXLU4472598', 'TLLU5203901', 'MSMU8333318']
        self.enterContainer(container)
        result = self.extract_containers()
        print(result)