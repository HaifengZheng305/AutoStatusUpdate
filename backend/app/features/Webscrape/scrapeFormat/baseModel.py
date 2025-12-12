from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, Literal

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
)
import time



TerminalName = Literal["MAHER", "APM", "PNCT"]


class BaseTerminalScraper(ABC):
    """
    Common interface for all terminal scrapers.
    Each concrete scraper knows how to scrape its own website.
    """

    def __init__(self, driver=None, containers = None,  session=None):
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
        el = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))
        el.clear()
        el.click()
        el.send_keys(text)
        return el

    def wait_xpath(self, xpath:str):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)
            )
        )

    def get(self, url):
        self.driver.get(url)
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
