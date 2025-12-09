from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, Literal

from selenium.webdriver.remote.webdriver import WebDriver


TerminalName = Literal["MAHER", "APM", "PNCT"]


class BaseTerminalScraper(ABC):
    """
    Common interface for all terminal scrapers.
    Each concrete scraper knows how to scrape its own website.
    """

    def __init__(self, terminal: TerminalName, driver=None, session=None):
        self.terminal = terminal
        self.driver = driver      # Selenium WebDriver (optional)
        self.session = session    # requests.Session (optional)

    @abstractmethod
    def scrape_container_status(self, container_id: str) -> dict:
        """
        Scrape and return container status information as a dict.
        """
        raise NotImplementedError


class MaherScraper(BaseTerminalScraper):
    def __init__(self, driver=None, session=None):
        super().__init__("MAHER", driver, session)

    def scrape_container_status(self, container_id: str) -> dict:
        # ---- Example logic (replace with real Maher scraping) ----
        # self.driver.get("https://www.maherterminals.com/track")
        # search_box = self.driver.find_element(...)
        # search_box.send_keys(container_id)
        # ...
        # Parse HTML, build dict
        return {
            "terminal": self.terminal,
            "container_id": container_id,
            "status": "AVAILABLE",
            "eta": "2025-12-10",
        }


class APMScraper(BaseTerminalScraper):
    def __init__(self, driver=None, session=None):
        super().__init__("APM", driver, session)

    def scrape_container_status(self, container_id: str) -> dict:
        # ---- Example logic for APM ----
        # self.driver.get("https://www.apmterminals.com/track")
        # ...
        return {
            "terminal": self.terminal,
            "container_id": container_id,
            "status": "ON_VESSEL",
            "eta": "2025-12-12",
        }


class PNCTScraper(BaseTerminalScraper):
    def __init__(self, driver=None, session=None):
        super().__init__("PNCT", driver, session)

    def scrape_container_status(self, container_id: str) -> dict:
        # ---- Example logic for PNCT ----
        # self.driver.get("https://www.pnct.com/track")
        # ...
        return {
            "terminal": self.terminal,
            "container_id": container_id,
            "status": "DISCHARGED",
            "eta": "2025-12-09",
        }


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


# =======================
# Example usage
# =======================

if __name__ == "__main__":
    # Example: single Selenium driver reused for all terminals
    # from selenium import webdriver
    # driver = webdriver.Chrome()

    driver = None  # replace with real driver if using Selenium

    terminal_name = "Maher"  # could come from DB, API, user input
    container_id = "MSKU1234567"

    scraper = TerminalScraperFactory.get_scraper(
        terminal=terminal_name,
        driver=driver,
    )

    data = scraper.scrape_container_status(container_id)
    print(data)