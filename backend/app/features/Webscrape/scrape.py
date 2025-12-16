from scrapeFormat.maher import MaherScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    maherLogin = os.getenv("maherLogin")
    maherPW = os.getenv("maherPW")
    scraper = MaherScraper(driver, username=maherLogin, password=maherPW)
    scraper.scrape()

if __name__ == "__main__":
    main()
