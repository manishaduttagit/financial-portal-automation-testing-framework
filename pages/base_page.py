from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver: WebDriver):
        """Initializes the base page with the browser driver session."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Standard 10-second smart explicit wait

    def open_url(self, url: str):
        """Navigates the browser to a specific web address."""
        self.driver.get(url)

    def find_element(self, locator: tuple):
        """Waits for an element to be visible on the screen before returning it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click_element(self, locator: tuple):
        """Waits for an element to be clickable, then clicks it."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator: tuple, text: str):
        """Clears an input field and types text into it safely."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)