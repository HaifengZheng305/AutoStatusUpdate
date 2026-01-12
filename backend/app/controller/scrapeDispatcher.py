import os
import asyncio
from typing import List

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app.features.Webscrape.scrapers.maher import MaherScraper
from app.features.Webscrape.scrapers.pnct import PNCTScraper
from app.models.container import Container, TerminalName


class ScraperRunner:
    def __init__(self, containers: List[Container] = None):
        load_dotenv()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.containers = containers or []

    async def run_maher(self):
        maher_containers = [c for c in self.containers if c.terminal == TerminalName.MAHER]
        
        if not maher_containers:
            return []

        maher_login = os.getenv("maherLogin")
        maher_pw = os.getenv("maherPW")

        if not maher_login or not maher_pw:
            raise RuntimeError("Maher credentials missing")

        maher = MaherScraper(
            self.driver,
            username=maher_login,
            password=maher_pw,
            containers=maher_containers
        )

        scraped_containers = maher.scrape_container_status()

        for container in scraped_containers:
            container.check = (
                container.available is True and
                container.customs_release is True and
                container.freight_release is True and
                container.last_free_day is not None
            )

        return scraped_containers

    async def run_pnct(self):
        pnct_containers = [c for c in self.containers if c.terminal == TerminalName.PNCT]
        
        if not pnct_containers:
            return []

        pnct = PNCTScraper(self.driver, pnct_containers)
        scraped_containers = pnct.scrape_container_status()
        
        for container in scraped_containers:
            container.check = (
                container.available is True and
                container.customs_release is True and
                container.freight_release is True and
                container.last_free_day is not None
            )

        return scraped_containers

    async def run(self) -> List[Container]:
        try:
            results: List[Container] = []

            if any(c.terminal == TerminalName.MAHER for c in self.containers):
                results.extend(await self.run_maher())

            if any(c.terminal == TerminalName.PNCT for c in self.containers):
                results.extend(await self.run_pnct())

            return results
        finally:
            self.driver.quit()

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(ScraperRunner().run())

