from scrapeFormat.maher import MaherScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    scraper = MaherScraper(driver, username="ANDYZ", password="andy@123")
    scraper.script_login()

if __name__ == "__main__":
    main()
