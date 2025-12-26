from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, Literal, List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)
import time


TerminalName = Literal["MAHER", "APM", "PNCT"]


class BaseTerminalScraper(ABC):
    """
    Common interface for all terminal scrapers.
    Each concrete scraper knows how to scrape its own website.
    """

    def __init__(self, driver=None, containers: Optional[List] = None,  session=None):
        self.driver = driver      # Selenium WebDriver (optional)
        self.wait = WebDriverWait(driver, 20)    # requests.Session (optional)
        self.containers = containers

    def click_element(self, css):
        el = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        el.click()
        return el

    def click_xpath(self, xpath: str, retries: int = 3):
        """
        Click an element located by XPath, with retries to handle
        StaleElementReferenceException from Angular re-rendering.
        """
        last_exc = None
        for attempt in range(retries):
            try:
                el = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                el.click()
                return el
            except StaleElementReferenceException as e:
                last_exc = e
                print(f"[click_xpath] Stale element for {xpath}, retry {attempt + 1}/{retries}")
        # If it still fails after retries, re-raise
        raise last_exc

    def type(self, css, text):
        el = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        el.clear()
        el.click()
        el.send_keys(text)
        return el
    
    def type_xpath(self, xpath, text):
        el = self.wait.until( EC.presence_of_element_located((By.XPATH, xpath))
        )

        # Ensure element is in view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", el
        )

        el.clear()
        el.send_keys(text)
        return el

    def wait_xpath(self, xpath:str):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)
            )
        )
    
    def wait_CSS(self, css:str):
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css))
        )

    def get(self, url):
        self.driver.get(url)

    def select_xpath(self, selectID, selectValue):
        select_el = self.wait.until(
            EC.presence_of_element_located((By.ID, selectID))
        )

        # Set value + notify MDB / Angular
        self.driver.execute_script(
            """
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """,
            select_el,
            selectValue
        )

    def ensure_expanded_xpath(self, header_xpath, inner_xpath, timeout=10):
        """
        Ensure an expandable section (accordion/panel/expander) is expanded.
        All locators are XPATH strings.
        - header_xpath: xpath to the clickable header/toggle
        - inner_xpath: xpath to an element that exists only when expanded (e.g. a button inside)
        Returns the located inner element (WebElement) when visible/clickable.
        Raises TimeoutException on failure.
        """
        wait = WebDriverWait(self.driver, timeout)

        # 1) quick check: if inner element is already visible -> return it
        try:
            print("step 1")
            return wait.until(EC.visibility_of_element_located((By.XPATH, inner_xpath)))
        except TimeoutException:
            pass  # not visible yet

        # 2) find header (may be stale so handle exceptions)
        try:
            print("step 2")
            header = self.driver.find_element(By.XPATH, header_xpath)
        except NoSuchElementException:
            raise NoSuchElementException(f"Header not found for xpath: {header_xpath}")

        # 3) try to infer expanded state from attributes or class (common patterns)
        try:
            print("step 3")
            aria = header.get_attribute("aria-expanded")
            cls = header.get_attribute("class") or ""
            # if header reports expanded or has typical 'expanded' class, wait for inner content
            if (aria and aria.lower() == "true") or ("expanded" in cls) or ("mat-expanded" in cls):
                return wait.until(EC.visibility_of_element_located((By.XPATH, inner_xpath)))
        except StaleElementReferenceException:
            # header went stale, we'll refetch and click below
            pass

        # 4) Not expanded — try clicking the header to expand.
        try:
            print("step 4")
            try:
            
                header.click()
            except (ElementClickInterceptedException, StaleElementReferenceException):
                # refetch header and try JS click fallback
                header = self.driver.find_element(By.XPATH, header_xpath)
                self.driver.execute_script("arguments[0].click();", header)

            # 5) wait for the inner element to be visible
            print("step 5")
            return wait.until(EC.visibility_of_element_located((By.XPATH, inner_xpath)))

        except TimeoutException:
            # If waiting failed, try one last strategy: scroll header into view and retry click
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", header)
                self.driver.execute_script("arguments[0].click();", header)
                return wait.until(EC.visibility_of_element_located((By.XPATH, inner_xpath)))
            except Exception as e:
                raise TimeoutException(
                    f"Failed to expand panel. header_xpath={header_xpath}, inner_xpath={inner_xpath}. Last error: {e}"
                )
    @abstractmethod
    def scrape_container_status(self, container_id: str) -> dict:
        """
        Scrape and return container status information as a dict.
        """
        raise NotImplementedError


'''
class TerminalScraperFactory:
    """
    Chooses the correct scraper implementation dynamically
    based on the terminal name.
    """

    _registry: Dict[TerminalName, Type[BaseTerminalScraper]] = {
        "MAHER": MaherScraper,
        "APM": APMScraper,
        "PNCT": PNCTScraper,
    }

    @classmethod
    def get_scraper(
        cls,
        terminal: str,
        driver=None,
        session=None,
    ) -> BaseTerminalScraper:
        # Normalize terminal input
        key = terminal.strip().upper()

        if key not in cls._registry:
            raise ValueError(f"Unsupported terminal: {terminal}")

        scraper_class = cls._registry[key]
        return scraper_class(driver=driver, session=session)
'''
