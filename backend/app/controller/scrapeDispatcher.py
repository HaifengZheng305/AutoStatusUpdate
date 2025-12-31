import os
import asyncio

from dotenv import load_dotenv

from pymongo.synchronous import collection
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app.features.Webscrape.scrapers.maher import MaherScraper
from app.features.Webscrape.scrapers.pnct import PNCTScraper

from app.repositories.container_repo import update_container_by_number, get_unchecked_containers_by_terminal
from app.db.mongo import get_container_collection, get_db_client


class ScraperRunner:
    def __init__(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

        self.client = get_db_client()
        self.containers_collection = get_container_collection(self.client)

    async def run_maher(self):
        maher_containers = await get_unchecked_containers_by_terminal(
            self.containers_collection,
            "MAHER"
        )
        maher_login = os.getenv("maherLogin")
        maher_pw = os.getenv("maherPW")

        if not maher_login or not maher_pw:
            raise RuntimeError("Maher credentials missing")

        maher = MaherScraper(
            self.driver,
            username=maher_login,
            password=maher_pw,
            containers = maher_containers
        )

        containers = maher.scrape_container_status()

        for container in containers:
            container.check = (
                container.available is True and
                container.customs_release is True and
                container.freight_release is True and
                container.last_free_day is not None
            )
            result = await update_container_by_number(
                container_number=container.container_number,
                container=container,
                collection=self.containers_collection
            )

            if not result:
                print(f"Container not found: {container.container_number}")


    async def run_pnct(self):
        pnct_containers = await get_unchecked_containers_by_terminal(
            self.containers_collection,
            "PNCT"
        )
        pnct = PNCTScraper(self.driver, pnct_containers)
        containers = pnct.scrape_container_status()
        for container in containers:
            container.check = (
                container.available is True and
                container.customs_release is True and
                container.freight_release is True and
                container.last_free_day is not None
            )
            result = await update_container_by_number(
                container_number=container.container_number,
                container=container,
                collection=self.containers_collection
            )

            if not result:
                print(f"Container not found: {container.container_number}")


    async def run(self):
        try:
            await self.run_maher()
            await self.run_pnct()
        finally:
            self.driver.quit()

# # class ScraperDispatcher:

# #     _registry: Dict[TerminalName, Type[BaseTerminalScraper]] = {
# #         "MAHER": MaherScraper,
# #         ##"APM": APMScraper,
# #         ##"PNCT": PNCTScraper,
# #     }

# #     @classmethod
# #     def run(cls, container: Container) -> dict:
# #         scraper_cls = cls._registry.get(container.terminal)

# #         if not scraper_cls:
# #             raise ValueError(f"No scraper registered for terminal {container.terminal}")

# #         scraper = scraper_cls()
# #         return scraper.scrape(container)


# async def main():
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     client = get_db_client()
#     containers_collection = get_container_collection(client)

#     try:
#         # Maher
#         maherLogin = os.getenv("maherLogin")
#         maherPW = os.getenv("maherPW")

#         if not maherLogin or not maherPW:
#             raise RuntimeError("Maher credentials missing")

#         maher = MaherScraper(driver, username=maherLogin, password=maherPW)
#         maherContainer = maher.scrape_container_status()

#         for container in maherContainer:
#             result = await update_container_by_number(
#                 container_number=container.container_number,
#                 container=container,
#                 collection=containers_collection
#             )

#             if not result:
#                 print(f"Container not found: {container.container_number}")


#         # Reset browser state
#         driver.delete_all_cookies()

#         # PNCT
#         pnct = PNCTScraper(driver)
#         pnctContainer = pnct.scrape_container_status()

#         for container in pnctContainer:
#             result = await update_container_by_number(
#                 container_number=container.container_number,
#                 container=container,
#                 collection=containers_collection
#             )

#             if not result:
#                 print(f"Container not found: {container.container_number}")

#     finally:
#         driver.quit()

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(ScraperRunner().run())

