from app.features.Webscrape.scrapers.maher import MaherScraper
from app.features.Webscrape.scrapers.pnct import PNCTScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# from models import TerminalName
# from scrapers.baseModel import BaseTerminalScraper, Container
from typing import Dict, Type
import os

load_dotenv()

# class ScraperDispatcher:

#     _registry: Dict[TerminalName, Type[BaseTerminalScraper]] = {
#         "MAHER": MaherScraper,
#         ##"APM": APMScraper,
#         ##"PNCT": PNCTScraper,
#     }

#     @classmethod
#     def run(cls, container: Container) -> dict:
#         scraper_cls = cls._registry.get(container.terminal)

#         if not scraper_cls:
#             raise ValueError(f"No scraper registered for terminal {container.terminal}")

#         scraper = scraper_cls()
#         return scraper.scrape(container)


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Maher
        maherLogin = os.getenv("maherLogin")
        maherPW = os.getenv("maherPW")

        if not maherLogin or not maherPW:
            raise RuntimeError("Maher credentials missing")

        maher = MaherScraper(driver, username=maherLogin, password=maherPW)
        maher.scrape_container_status()

        # Reset browser state
        driver.delete_all_cookies()

        # PNCT
        pnct = PNCTScraper(driver)
        pnct.scrape_container_status()


    finally:
        driver.quit()

if __name__ == "__main__":
    main()
