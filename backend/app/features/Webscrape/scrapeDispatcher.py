from scrapers.maher import MaherScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from models import TerminalName
from scrapers.baseModel import BaseTerminalScraper, Container
from typing import Dict, Type
import os

load_dotenv()

class ScraperDispatcher:

    _registry: Dict[TerminalName, Type[BaseTerminalScraper]] = {
        "MAHER": MaherScraper,
        ##"APM": APMScraper,
        ##"PNCT": PNCTScraper,
    }

    @classmethod
    def run(cls, container: Container) -> dict:
        scraper_cls = cls._registry.get(container.terminal)

        if not scraper_cls:
            raise ValueError(f"No scraper registered for terminal {container.terminal}")

        scraper = scraper_cls()
        return scraper.scrape(container)


# def main():
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     maherLogin = os.getenv("maherLogin")
#     maherPW = os.getenv("maherPW")
#     scraper = MaherScraper(driver, username=maherLogin, password=maherPW)
#     scraper.scrape()

# if __name__ == "__main__":
#     main()
