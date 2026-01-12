import asyncio
from app.controller.scrapeDispatcher import ScraperRunner
from app.models.container import Container, TerminalName

async def main():
    containers = [
        Container(
            container_number="MSCU1234567",
            terminal=TerminalName.MAHER,
            available=False,
            customs_release=False,
            freight_release=False,
            last_free_day=None
        ),
        Container(
            container_number="OOLU7654321",
            terminal=TerminalName.PNCT,
            available=False,
            customs_release=False,
            freight_release=False,
            last_free_day=None
        ),
    ]

    runner = ScraperRunner(containers)
    scraped_containers = await runner.run()

    # Send to Google Sheets
    # update_google_sheet(scraped_containers)  # TODO: Implement this function

if __name__ == "__main__":
    asyncio.run(main())