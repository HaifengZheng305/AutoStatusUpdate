from app.features.Webscrape.scrapers.maher import MaherScraper
from app.features.Webscrape.scrapers.pnct import PNCTScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from app.repositories.container_repo import update_container_by_number
from app.db.mongo import get_container_collection, get_db_client
import asyncio

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


async def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    client = get_db_client()
    containers_collection = get_container_collection(client)

    try:
        # Maher
        maherLogin = os.getenv("maherLogin")
        maherPW = os.getenv("maherPW")

        if not maherLogin or not maherPW:
            raise RuntimeError("Maher credentials missing")

        maher = MaherScraper(driver, username=maherLogin, password=maherPW)
        maherContainer = maher.scrape_container_status()

        for container in maherContainer:
            result = await update_container_by_number(
                container_number=container.container_number,
                container=container,
                collection=containers_collection
            )

            if not result:
                print(f"Container not found: {container.container_number}")


        # Reset browser state
        driver.delete_all_cookies()

        # PNCT
        pnct = PNCTScraper(driver)
        pnctContainer = pnct.scrape_container_status()

        for container in pnctContainer:
            result = await update_container_by_number(
                container_number=container.container_number,
                container=container,
                collection=containers_collection
            )

            if not result:
                print(f"Container not found: {container.container_number}")

    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
