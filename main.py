from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from login import LinkedinLogin
from linkedin_profile_search import LinkedinSearch
from excel_creator import ExcelCreator
import os
import sys
from typing import Tuple
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ScrapingConfig:
    search_term: str
    max_profiles: int

class ArgumentValidator:
    def validate_args(self, args: list) -> ScrapingConfig:
        if len(args) != 3:
            raise ValueError(
                "Invalid number of arguments. This program requires exactly 2 arguments:\n\n" 
                "1. Search keyword (in quotes)\n" 
                "2. Number of profiles to search\n\n" 
                "Example usage:\n" 
                "python main.py \"Software Engineer\" 100    # Search for 'Software Engineer' and get 100 profiles\n" 
                "python main.py \"Data Scientist\" 50     # Search for 'Data Scientist' and get 50 profiles\n"
            )

        search_term = args[1]
        try:
            max_profiles = int(args[2])
            if max_profiles <= 0:
                raise ValueError("Profile count must be a positive number")
        except ValueError:
            raise ValueError(f"Invalid profile count: {args[2]}. Must be a positive number.")

        return ScrapingConfig(search_term=search_term, max_profiles=max_profiles)

class BrowserManager:
    @staticmethod
    def create_firefox_options() -> Options:
        firefox_options = Options()
        firefox_options.add_argument("--disable-notifications") 
        firefox_options.add_argument("--disable-gpu")  
        firefox_options.page_load_strategy = 'normal'  
        return firefox_options

    @staticmethod
    def create_driver() -> webdriver.Firefox:
        print("Configuring Firefox settings...")
        options = BrowserManager.create_firefox_options()
        print("Starting Firefox...")
        return webdriver.Firefox(options=options)

    @staticmethod
    def close_driver(driver: Optional[webdriver.Firefox]) -> None:
        if driver:
            try:
                driver.quit()
                print("Browser closed.")
            except Exception as e:
                print(f"Error closing browser: {str(e)}")

class LinkedinScraper:
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.driver = None

    def initialize_browser(self) -> None:
        self.driver = BrowserManager.create_driver()

    def run_scraping(self) -> None:
        try:
            print(f"Search term: {self.config.search_term}")
            print(f"Max profiles: {self.config.max_profiles}")

            print("Login process is starting...")
            login_manager = LinkedinLogin(self.driver)

            if not login_manager.login():
                print("Login failed! Please check your credentials.")
                return

            print("Search process is starting...")
            profile_search = LinkedinSearch(self.driver)
            profiles = profile_search.search_profiles(self.config.search_term, self.config.max_profiles)

            if not profiles or len(profiles) == 0:
                print("No profiles found.")
                return

            print(f"\n{len(profiles)} profiles found.")
            self._export_profiles(profiles)

        except Exception as e:
            print(f"An error occurred while running the program: {str(e)}")

    def _export_profiles(self, profiles: List) -> None:
        excel_creator = ExcelCreator()
        excel_file = excel_creator.export_profiles(profiles, self.config.search_term)

        if excel_file:
            print(f"Data successfully exported to {excel_file}")
        else:
            print("Failed to export data to Excel")

    def cleanup(self) -> None:
        input("Press Enter to close the browser...")
        BrowserManager.close_driver(self.driver)

def main():
    try:
        validator = ArgumentValidator()
        config = validator.validate_args(sys.argv)

        scraper = LinkedinScraper(config)
        scraper.initialize_browser()
        scraper.run_scraping()
        scraper.cleanup()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
