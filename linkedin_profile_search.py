from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from excel_creator import ExcelCreator
import time

class LinkedinProfile:
    def __init__(self, name="", title="", location="", summary="", connections="", profile_link=""):
        self.name = name
        self.title = title
        self.location = location
        self.summary = summary
        self.connections = connections
        self.profile_link = profile_link

class LinkedinSearch:
    PROFILE_BASE_XPATH = "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[{index}]/div/div/div/div[2]"
    PROFILE_LINK_XPATH = "div[1]/div[1]/div/span[1]/span/a"
    NAME_XPATH = "div[1]/div[1]/div/span[1]/span/a/span/span[1]"
    TITLE_XPATH = "div[1]/div[2]"
    LOCATION_XPATH = "div[1]/div[3]"
    CONNECTIONS_XPATH = "div[2]/div/div[2]/span"
    SUMMARY_XPATH = "p"
    NEXT_BUTTON_SELECTORS = [
        "//button[@aria-label='Next']",
        "//button[contains(@class, 'artdeco-pagination__button--next')]"
    ]

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.profiles = []

    def _wait_for_element(self, by, value, timeout=10, element=None):
        try:
            wait_condition = EC.presence_of_element_located((by, value))
            if element:
                return WebDriverWait(element, timeout).until(wait_condition)
            
            element = WebDriverWait(self.driver, timeout).until(wait_condition)
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of(element)
            )
            return element
        except TimeoutException:
            return None

    def _safe_get_element_text(self, element, default="N/A"):
        if not element:
            return default
        text = element.text.strip()
        return text if text else default

    def _extract_profile_data(self, base_xpath):
        try:
            profile = LinkedinProfile()
            
            try:
                link_element = self.driver.find_element(By.XPATH, f"{base_xpath}/{self.PROFILE_LINK_XPATH}")
                profile_link = link_element.get_attribute("href")
                profile.profile_link = "N/A" if "headless?origin=OTHER&keywords=" in profile_link else profile_link
                
                name_element = self.driver.find_element(By.XPATH, f"{base_xpath}/{self.NAME_XPATH}")
                profile.name = name_element.text.strip()
            except NoSuchElementException:
                profile.name = "N/A"
            
            try:
                title_element = self.driver.find_element(By.XPATH, f"{base_xpath}/{self.TITLE_XPATH}")
                profile.title = title_element.text.strip()
            except NoSuchElementException:
                profile.title = "N/A"
            
            try:
                location_element = self.driver.find_element(By.XPATH, f"{base_xpath}/{self.LOCATION_XPATH}")
                profile.location = location_element.text.strip()
            except NoSuchElementException:
                profile.location = "N/A"
            
            try:
                connections_element = self.driver.find_element(By.XPATH, f"{base_xpath}/{self.CONNECTIONS_XPATH}")
                profile.connections = connections_element.text.strip()
            except NoSuchElementException:
                profile.connections = "N/A"

            try:
                summary_element = self.driver.find_element(By.XPATH, f"{base_xpath}/{self.SUMMARY_XPATH}")
                profile.summary = summary_element.text.strip()
            except NoSuchElementException:
                profile.summary = "N/A"
            
            if profile.name != "N/A" or (profile.profile_link and not profile.profile_link.isspace()):
                return profile
            return None

        except Exception as e:
            print(f"Error extracting profile data: {str(e)}")
            return None

    def search_profiles(self, search_term, max_profiles=100):
        try:
            profiles_per_page = 10
            pages_to_scrape = (max_profiles + profiles_per_page - 1) // profiles_per_page
            excel_creator = ExcelCreator()
            
            print(f"Searching for '{search_term}' and collecting {max_profiles} profiles ({pages_to_scrape} pages)")
            self.driver.get(f"https://www.linkedin.com/search/results/people/?keywords={search_term}")
            time.sleep(5)
            self._wait_for_element(By.XPATH, "//div[contains(@class, 'search-results-container')]")
            
            page_count = 0
            profile_count = 0
            
            while profile_count < max_profiles:
                page_count += 1
                print(f"\nScanning page {page_count}...")
                
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                
                remaining_profiles = max_profiles - profile_count
                profiles_to_extract = min(10, remaining_profiles)
                
                page_profiles = self._extract_profiles_from_page(profiles_to_extract)
                if page_profiles:
                    self.profiles.extend(page_profiles)
                    profile_count += len(page_profiles)
                    print(f"Found and added {len(page_profiles)} profiles from page {page_count}. Total: {profile_count}")
                
                if profile_count >= max_profiles:
                    break
                    
                if not self._go_to_next_page():
                    print("No more pages available")
                    break
                
                time.sleep(3) 
            
            print(f"\nSearch completed. Found and saved {profile_count} profiles.")
            return self.profiles

        except Exception as e:
            print(f"Error occurred during profile search: {str(e)}")
            return 0

    def _extract_profiles_from_page(self, profiles_to_extract=10):
        page_profiles = []
        time.sleep(2)
        for i in range(1, profiles_to_extract + 1):
            try:
                base_xpath = self.PROFILE_BASE_XPATH.format(index=i)
                profile = self._extract_profile_data(base_xpath)
                if profile:
                    page_profiles.append(profile)
                    print(f"Profile {i}: {profile.name} - {profile.title}")
                else:
                    print(f"Profile {i}: Could not extract valid profile data")
            except Exception as e:
                print(f"Error processing profile {i}: {str(e)}")
                continue
        return page_profiles if page_profiles else []

    def _go_to_next_page(self):
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            for selector in self.NEXT_BUTTON_SELECTORS:
                next_button = self._wait_for_element(By.XPATH, selector, timeout=5)
                if next_button and next_button.is_enabled():
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(1)
                    next_button.click()
                    print("Moving to next page...")
                    time.sleep(3)
                    return True
            
            print("No more pages found")
            return False

        except Exception as e:
            print(f"Error during page transition: {str(e)}")
            return False
