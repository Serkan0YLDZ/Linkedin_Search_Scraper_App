from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pathlib import Path
import json
import os
import time
from dotenv import load_dotenv
from selenium.webdriver.firefox.options import Options

class LinkedinLogin:
    def __init__(self, driver):
        self.driver = driver
        self.cookies_dir = "cookies"
        self.cookies_file = os.path.join(self.cookies_dir, "linkedin_cookies.json")
        self.wait = WebDriverWait(driver, 10)
        
        load_dotenv()

        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not email or not password:
            raise ValueError("LINKEDIN_EMAIL or LINKEDIN_PASSWORD environment variables not found!")

        self.credentials = {
            "email": email,
            "password": password
        }

    def _handle_operation(self, operation_name, operation_func):
        try:
            return operation_func()
        except Exception as e:
            print(f"Error during {operation_name}: {str(e)}")
            return False

    def save_cookies(self):
        def _save():
            cookies = self.driver.get_cookies()
            if not cookies:
                print("WARNING: No cookies were retrieved!")
                return False

            Path(self.cookies_dir).mkdir(exist_ok=True)
            with open(self.cookies_file, "w") as f:
                json.dump(cookies, f)
            print("Cookies saved successfully.")
            return True

        return self._handle_operation("saving cookies", _save)

    def load_cookies(self):
        def _load():
            if not os.path.exists(self.cookies_file):
                print("Cookie file not found.")
                return False

            with open(self.cookies_file, "r") as f:
                cookies = json.load(f)

            if not cookies:
                print("Cookie file is empty or invalid.")
                return False

            self.driver.get("https://www.linkedin.com")
            print("Linkedin homepage loaded.")
            time.sleep(5)

            for cookie in cookies:
                try:
                    if 'expiry' in cookie and isinstance(cookie['expiry'], float):
                        cookie['expiry'] = int(cookie['expiry'])
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Error adding cookie: {str(e)}")

            self.driver.refresh()
            time.sleep(3)

            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
            except TimeoutException:
                print("Page failed to load completely after refresh")
                return False

            current_url = self.driver.current_url
            if self._is_logged_in_url(current_url):
                print("Login successful with cookies.")
                return True

            print("Cookie login failed.")
            return False

        return self._handle_operation("loading cookies", _load)

    def _is_logged_in_url(self, url):
        return any(url_part in url for url_part in ["feed", "mynetwork", "messaging", "notifications"])

    def _wait_for_element(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"Element not found: {value}")
            return None

    def login(self):
        def _login():
            if self.load_cookies():
                return True

            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)

            email_field = self._wait_for_element(By.ID, "username")
            password_field = self._wait_for_element(By.ID, "password")

            if not email_field or not password_field:
                print("Login form elements not found. Retrying after refresh...")
                self.driver.refresh()
                time.sleep(3)
                email_field = self._wait_for_element(By.ID, "username")
                password_field = self._wait_for_element(By.ID, "password")
                if not email_field or not password_field:
                    return False

            email_field.send_keys(self.credentials["email"])
            password_field.send_keys(self.credentials["password"])

            login_button = self._wait_for_element(By.CSS_SELECTOR, "button[type='submit']")
            if not login_button:
                return False

            login_button.click()
            time.sleep(5)

            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
            except TimeoutException:
                print("Page failed to load completely after login")
                return False

            if self._is_logged_in_url(self.driver.current_url):
                self.save_cookies()
                return True

            return False

        return self._handle_operation("login", _login)

def create_firefox_driver():
    options = Options()
    options.headless = False
    driver = webdriver.Firefox(options=options)
    return driver
